# This file is part of dotmgr.
#
# dotmgr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dotmgr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dotmgr.  If not, see <http://www.gnu.org/licenses/>.
"""A module for dotfile management classes and service functions.
"""

from getpass import getuser
from os import listdir, makedirs, remove, symlink
from os.path import dirname, exists, expanduser, isdir, islink, join
from shutil import move, rmtree
from socket import gethostname

from dotmgr.transformer import Transformer


class Manager(object):
    """An instance of this class can be used to manage dotfiles.

    Attributes:
        dotfile_repository:      The dotfile repository.
        dotfile_stage_path:      The absolute path to the dotfile stage directory.
        dotfile_tag_config_path: The absolute path to the dotfile tag configuration file.
        verbose:                 If set to `True`, debug messages are generated.
    """

    def __init__(self, repository, stage_path, tag_config_path, verbose):
        self.dotfile_repository = repository
        self.dotfile_stage_path = stage_path
        self.dotfile_tag_config_path = tag_config_path
        self.verbose = verbose
        self._user = getuser()
        self._tags = self._get_tags()

    def _get_tags(self):
        """Parses the dotmgr config file and extracts the tags for the current host.

        Reads the hostname and searches the dotmgr config for a line defining tags for the host.

        Returns:
            The tags defined for the current host.
        """
        hostname = gethostname()
        tag_config = None
        with open(self.dotfile_tag_config_path, encoding='utf-8') as config:
            tag_config = config.readlines()

        for line in tag_config:
            if line.startswith(hostname + ':'):
                tags = line.split(':')[1]
                tags = tags.split()
                if self.verbose:
                    print('Found tags: {}'.format(', '.join(tags)))
                return tags
        print('Warning: No tags found for this machine!')
        return [""]

    def _perform_on_stage(self, action, *args):
        """Performs the given action on all dotfiles on stage.

        Args:
            action: The action to perform.
            args:   The arguments to the action.
        """
        for entry in listdir(self.dotfile_stage_path):
            if isdir(self.stage_path(entry)):
                self._recurse_stage_directory(entry, action, *args)
            else:
                action(entry, *args)

    def _recurse_stage_directory(self, directory_path, action, *args):
        """Performs an action on dotfiles on stage.

        Args:
            directory_path: The relative path to the directory to link.
            action: The action to perform.
            args:   The arguments to the action.
        """
        for entry in listdir(self.stage_path(directory_path)):
            full_path = join(directory_path, entry)
            if isdir(self.stage_path(full_path)):
                self._recurse_stage_directory(full_path, action, *args)
            else:
                action(full_path, *args)

    def _specialize_directory(self, directory_path, link):
        """Recursively specializes a directory of dotfiles from the repository.

        Args:
            directory_path: The relative path to the directory to specialize.
            link: If set to `True`, symlinks pointing to the staged files are also created in the
                  user's home directory.
        """
        for entry in listdir(self.repo_path(directory_path)):
            if entry == '.git':
                continue
            full_path = join(directory_path, entry)
            if isdir(self.repo_path(full_path)):
                self._specialize_directory(full_path, link)
            else:
                self.specialize(full_path, link)

    def add(self, dotfile_path, commit):
        """Moves and links a dotfile from the home directory to the stage and generalizes it.

        Args:
            dotfile_path: The relative path to the dotfile to add.
            commit:       If `True`, the new dotfile is automatically committed to the repository.
        """
        source = home_path(dotfile_path)
        if islink(source):
            if self.verbose:
                print('File {} is a symlink. It seems it is already managed. \\o/'.format(source))
        else:
            destination = self.stage_path(dotfile_path)
            print('Moving dotfile   {} => {}'.format(source, destination))
            makedirs(dirname(destination), exist_ok=True)
            move(source, destination)
            self.link(dotfile_path)
            self.generalize(dotfile_path, False)

        if commit:
            self.dotfile_repository.add(dotfile_path)

    def delete(self, dotfile_path, rm_repo, commit):
        """Removes a dotfile from the stage and the symlink from $HOME.

        Args:
            dotfile_path: The relative path to the dotfile to remove.
            rm_repo:      If `True`, the dotfile is also deleted from the repository.
            commit:       If `True`, the removal is automatically committed to the repository.
        """
        print('Removing {} and its symlink'.format(dotfile_path))
        try:
            remove(home_path(dotfile_path))
        except FileNotFoundError:
            print('Warning: Symlink for {} not found'.format(dotfile_path))

        try:
            remove(self.stage_path(dotfile_path))
        except FileNotFoundError:
            print('Warning: {} is not on stage'.format(dotfile_path))

        if rm_repo or commit:
            print('Removing {} from repository'.format(dotfile_path))
            try:
                remove(self.repo_path(dotfile_path))
            except FileNotFoundError:
                print('Warning: {} is not in the repository'.format(dotfile_path))

        if commit:
            self.dotfile_repository.remove(dotfile_path)

    def delete_all(self):
        """Removes all symlinks to staged files as well as the files themselves.
        """
        print('Cleaning')
        self._perform_on_stage(self.delete, False, False)
        rmtree(self.dotfile_stage_path)

    def generalize(self, dotfile_path, commit, message=None):
        """Generalizes a dotfile from the stage.

        Identifies and un-comments blocks deactivated for this host.
        The generalized file is written to the repository.

        Args:
            dotfile_path: The relative path to the dotfile to generalize.
            commit:       If `True`, the changes are automatically committed to the repository.
            message:      An optional commit message. If omitted, a default message is generated.
        """

        print('Generalizing ' + dotfile_path)
        specific_content = None
        try:
            with open(self.stage_path(dotfile_path), encoding='utf-8') as specific_dotfile:
                specific_content = specific_dotfile.readlines()
        except FileNotFoundError:
            print('It seems {0} is not handled by dotmgr.\n'
                  'You can add it with `dotmgr -A {0}`.'.format(dotfile_path))
        if not specific_content:
            return

        flt = Transformer(self._tags, self._user, self.verbose)
        generic_content = flt.generalize(specific_content)

        makedirs(self.repo_path(dirname(dotfile_path)), exist_ok=True)
        with open(self.repo_path(dotfile_path), 'w', encoding='utf-8') as dotfile:
            dotfile.write(generic_content)

        if commit:
            self.dotfile_repository.update(dotfile_path, message)

    def generalize_all(self, commit):
        """Generalizes all dotfiles on the stage and writes results to the repository.

        Args:
            commit: If `True`, the changes are automatically committed to the repository.
        """
        print('Generalizing all dotfiles')
        self._perform_on_stage(self.generalize, commit)

    def link(self, dotfile_path):
        """Links a dotfile from the stage to $HOME.

        Args:
            dotfile_path: The relative path to the dotfile to link.
        """
        link_path = home_path(dotfile_path)
        if exists(link_path):
            return

        dest_path = self.stage_path(dotfile_path)
        print("Creating symlink {} -> {}".format(link_path, dest_path))
        makedirs(dirname(link_path), exist_ok=True)
        symlink(dest_path, link_path)

    def link_all(self):
        """Creates missing symlinks to all dotfiles on stage.

        Also automagically creates missing folders in $HOME.
        """
        self._perform_on_stage(self.link)

    def repo_path(self, dotfile_name):
        """Returns the absolute path to a named dotfile in the repository.

        Args:
            dotfile_name: The name of the dotfile whose path should by synthesized.

        Returns:
            The absolute path to the dotfile in the repository.
        """
        return join(self.dotfile_repository.path, dotfile_name)

    def specialize(self, dotfile_path, link):
        """Specializes a dotfile from the repository.

        Identifies and comments out blocks not valid for this host.
        The specialized file is written to the stage directory.

        Args:
            dotfile_path: The relative path to the dotfile to specialize.
            link: If set to `True`, a symlink pointing to the specialized file is also created in
                  the user's home directory.
        """

        dotfile_content = None
        try:
            with open(self.repo_path(dotfile_path), encoding='utf-8') as generic_dotfile:
                dotfile_content = generic_dotfile.readlines()
        except FileNotFoundError:
            print('{0} is not in the specified dotfile repository. :-('.format(dotfile_path))
        if not dotfile_content:
            return

        flt = Transformer(self._tags, self._user, self.verbose)
        header_info = flt.parse_header(dotfile_content)
        if 'skip' in header_info and header_info['skip']:
            print('Skipping {} as requested in its header'.format(dotfile_path))
            return
        print('Specializing ' + dotfile_path)

        makedirs(self.stage_path(dirname(dotfile_path)), exist_ok=True)
        with open(self.stage_path(dotfile_path), 'w', encoding='utf-8') as dotfile:
            dotfile.write(flt.specialize(dotfile_content))

        if link:
            self.link(dotfile_path)

    def specialize_all(self, link):
        """Specializes all dotfiles in the repositroy and writes results to the stage.

        Args:
            link: If set to `True`, symlinks pointing to the staged files are also created in the
                  user's home directory.
        """

        print('Specializing all dotfiles')
        for entry in listdir(self.dotfile_repository.path):
            if entry == '.git':
                continue
            if isdir(join(self.dotfile_repository.path, entry)):
                if self.repo_path(entry) == self.dotfile_stage_path:
                    continue
                self._specialize_directory(entry, link)
            else:
                self.specialize(entry, link)

        if link:
            self.link_all()

    def stage_path(self, dotfile_name):
        """Returns the absolute path to a named dotfile on stage.

        Args:
            dotfile_name: The name of the dotfile whose path should by synthesized.

        Returns:
            The absolute stage path to the dotfile.
        """
        return join(self.dotfile_stage_path, dotfile_name)

def home_path(dotfile_name):
    """Returns the absolute path to a named dotfile in the user's $HOME directory.

    Args:
        dotfile_name: The name of the dotfile whose path should by synthesized.

    Returns:
        The absolute path to the dotfile in the user's $HOME directory.
    """
    return expanduser('~/{}'.format(dotfile_name))
