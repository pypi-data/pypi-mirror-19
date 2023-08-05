"""Tests for the manager module.
"""
from copy import deepcopy
from os.path import dirname, expanduser
from unittest import TestCase
from unittest.mock import MagicMock, call, mock_open, patch

from dotmgr.manager import Manager, home_path
from dotmgr.transformer import Transformer


MOCKED_COMMIT_MESSAGE = 'This is an awesome commit message!'
MOCKED_DOTFILE_PATH = '.config/test/rc.conf'
MOCKED_FILE_LISTINGS = [
    ['.config', '.vimrc', '.zshrc'],
    ['so_program', 'such_config'],
    ['very_config', 'wow']
]
ASSERTED_FILE_PATHS = [
    '.config/so_program/very_config',
    '.config/so_program/wow',
    '.config/such_config',
    '.vimrc',
    '.zshrc'
]
MOCKED_HOSTNAME = 'testhost'
MOCKED_REPO_PATH = '/tmp/repository'
MOCKED_STAGE_PATH = '/tmp/stage'
MOCKED_TAG_CONFIG_PATH = '.config/dotmgr/tag.cfg'
MOCKED_TAGS = 'tag_one tag_two'
MOCKED_TAG_CONFIG = 'otherhost: tag_three\n' + MOCKED_HOSTNAME + ': ' + MOCKED_TAGS

class ManagerTest(TestCase):
    """Tests for the manager module.
    """

    def setUp(self):
        """Common setup tasks for tests in this unit.
        """
        self.repo_mock = MagicMock()
        self.repo_mock.path = MOCKED_REPO_PATH
        with patch.object(Manager, '_get_tags', return_value=MOCKED_TAGS.split()):
            self.mgr = Manager(self.repo_mock, MOCKED_STAGE_PATH, MOCKED_TAG_CONFIG_PATH, False)
        self.home_file_path = expanduser('~/') + MOCKED_DOTFILE_PATH
        self.stage_file_path = MOCKED_STAGE_PATH + '/' + MOCKED_DOTFILE_PATH
        self.repo_file_path = MOCKED_REPO_PATH + '/' + MOCKED_DOTFILE_PATH

        patcher = patch('builtins.open')
        self.open_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.listdir')
        self.ls_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.makedirs')
        self.mkdir_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.remove')
        self.rm_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.isdir')
        self.isdir_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.islink')
        self.islnk_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.symlink')
        self.ln_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.exists')
        self.exist_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.move')
        self.mv_mock = patcher.start()
        self.addCleanup(patcher.stop)
        patcher = patch('dotmgr.manager.rmtree')
        self.rmr_mock = patcher.start()
        self.addCleanup(patcher.stop)

    @patch('dotmgr.manager.gethostname')
    def test_get_tags(self, hostname_mock):
        """Tests _get_tags with a valid tag config.
        """
        hostname_mock.return_value = MOCKED_HOSTNAME
        mock_open(mock=self.open_mock, read_data=MOCKED_TAG_CONFIG)
        with patch('builtins.print'):
            self.assertEqual(MOCKED_TAGS.split(), self.mgr._get_tags())
        self.assertEqual(hostname_mock.call_count, 1)
        self.open_mock.assert_called_once_with(MOCKED_TAG_CONFIG_PATH, encoding='utf-8')

    @patch('dotmgr.manager.gethostname')
    def test_get_tags_not_found(self, hostname_mock):
        """Tests _get_tags with an empty tag config.
        """
        with patch('builtins.print'):
            self.assertEqual([''], self.mgr._get_tags())
        self.assertEqual(hostname_mock.call_count, 1)
        self.open_mock.assert_called_once_with(MOCKED_TAG_CONFIG_PATH, encoding='utf-8')

    @patch.object(Manager, 'generalize')
    @patch.object(Manager, 'link')
    @patch.object(Manager, 'stage_path')
    def test_add_existing(self, stagepath_mock, link_mock, generalize_mock):
        """Tests add with an already existing link.
        """
        self.islnk_mock.return_value = True
        with patch('dotmgr.manager.home_path'):
            self.mgr.add(MOCKED_DOTFILE_PATH, False)
        self.assertFalse(stagepath_mock.called)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(self.mv_mock.called)
        self.assertFalse(link_mock.called)
        self.assertFalse(generalize_mock.called)
        self.assertFalse(self.repo_mock.add.called)

    @patch.object(Manager, 'generalize')
    @patch.object(Manager, 'link')
    @patch.object(Manager, 'stage_path')
    @patch('dotmgr.manager.home_path')
    def test_add_new(self, homepath_mock, stagepath_mock, link_mock, generalize_mock):
        """Tests add.
        """
        homepath_mock.return_value = self.home_file_path
        self.islnk_mock.return_value = False
        stagepath_mock.return_value = self.stage_file_path
        with patch('builtins.print'):
            self.mgr.add(MOCKED_DOTFILE_PATH, False)
        stagepath_mock.assert_called_once_with(MOCKED_DOTFILE_PATH)
        self.mkdir_mock.assert_called_once_with(dirname(self.stage_file_path), exist_ok=True)
        self.mv_mock.assert_called_once_with(self.home_file_path, self.stage_file_path)
        link_mock.assert_called_once_with(MOCKED_DOTFILE_PATH)
        generalize_mock.assert_called_once_with(MOCKED_DOTFILE_PATH, False)
        self.assertFalse(self.repo_mock.add.called)

    @patch.object(Manager, 'generalize')
    @patch.object(Manager, 'link')
    @patch.object(Manager, 'stage_path')
    @patch('dotmgr.manager.home_path')
    def test_add_and_commit(self, homepath_mock, stagepath_mock, link_mock, generalize_mock):
        """Tests add with commit.
        """
        homepath = expanduser('~/') + MOCKED_DOTFILE_PATH
        stagepath = MOCKED_STAGE_PATH + '/' + MOCKED_DOTFILE_PATH
        homepath_mock.return_value = homepath
        self.islnk_mock.return_value = False
        stagepath_mock.return_value = stagepath
        with patch('builtins.print'):
            self.mgr.add(MOCKED_DOTFILE_PATH, True)
        stagepath_mock.assert_called_once_with(MOCKED_DOTFILE_PATH)
        self.mkdir_mock.assert_called_once_with(dirname(stagepath), exist_ok=True)
        self.mv_mock.assert_called_once_with(homepath, stagepath)
        link_mock.assert_called_once_with(MOCKED_DOTFILE_PATH)
        generalize_mock.assert_called_once_with(MOCKED_DOTFILE_PATH, False)
        self.repo_mock.add.assert_called_once_with(MOCKED_DOTFILE_PATH)

    def test_delete(self):
        """Tests delete.
        """
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, False, False)
        calls = [call(self.home_file_path), call(self.stage_file_path)]
        self.rm_mock.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.rm_mock.call_count, 2)
        self.assertFalse(self.repo_mock.remove.called)

    def test_delete_from_repo(self):
        """Tests delete with removal from repository.
        """
        self.rm_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, True, False)
        calls = [call(self.home_file_path),
                 call(self.stage_file_path),
                 call(self.repo_file_path)]
        self.rm_mock.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.rm_mock.call_count, 3)
        self.assertFalse(self.repo_mock.remove.called)

    def test_delete_and_commit(self):
        """Tests delete with removal from repository.
        """
        self.rm_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, False, True)
        calls = [call(self.home_file_path),
                 call(self.stage_file_path),
                 call(self.repo_file_path)]
        self.rm_mock.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.rm_mock.call_count, 3)
        self.repo_mock.remove.assert_called_once_with(MOCKED_DOTFILE_PATH)

    def test_delete_non_existing(self):
        """Tests delete with a non-existing dotfile.
        """
        self.rm_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.delete(MOCKED_DOTFILE_PATH, False, False)
        calls = [call(self.home_file_path), call(self.stage_file_path)]
        self.rm_mock.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.rm_mock.call_count, 2)
        self.assertFalse(self.repo_mock.remove.called)

    @patch.object(Manager, 'delete')
    def test_delete_all(self, delete_mock):
        """Tests delete_all.
        """
        self.ls_mock.side_effect = MOCKED_FILE_LISTINGS
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False]
        with patch('builtins.print'):
            self.mgr.delete_all()
        calls = map(lambda path: call(path, False, False), ASSERTED_FILE_PATHS)
        delete_mock.assert_has_calls(calls)
        self.rmr_mock.assert_called_once_with(MOCKED_STAGE_PATH)

    @patch.object(Transformer, 'generalize')
    def test_generalize(self, generalize_mock):
        """Tests generalize with an untracked file.
        """
        mock_open(mock=self.open_mock, read_data='line1\nline2')
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.assertFalse(self.repo_mock.update.called)

    @patch.object(Transformer, 'generalize')
    def test_generalize_and_commit(self, generalize_mock):
        """Tests generalizing and committing an untracked file.
        """
        mock_open(mock=self.open_mock, read_data='line1\nline2')
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, True)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.repo_mock.update.assert_called_once_with(MOCKED_DOTFILE_PATH, None)

    @patch.object(Transformer, 'generalize')
    def test_generalize_with_commit_msg(self, generalize_mock):
        """Tests generalizing and committing an untracked file with a custom commit message.
        """
        mock_open(mock=self.open_mock, read_data='line1\nline2')
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, True, message=MOCKED_COMMIT_MESSAGE)
        self.mkdir_mock.assert_called_once_with(dirname(self.repo_file_path), exist_ok=True)
        generalize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.repo_file_path, 'w', encoding='utf-8')])
        self.repo_mock.update.assert_called_once_with(MOCKED_DOTFILE_PATH, MOCKED_COMMIT_MESSAGE)

    @patch.object(Transformer, 'generalize')
    def test_generalize_non_existing(self, generalize_mock):
        """Tests generalize with a non-existing file.
        """
        self.open_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.generalize(MOCKED_DOTFILE_PATH, False)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(generalize_mock.called)
        self.assertEqual(self.open_mock.call_count, 1)
        self.assertFalse(self.repo_mock.update.called)

    @patch.object(Manager, 'generalize')
    def test_generalize_all(self, generalize_mock):
        """Tests generalize_all.
        """
        self.ls_mock.side_effect = MOCKED_FILE_LISTINGS
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False]
        with patch('builtins.print'):
            self.mgr.generalize_all(True)
        calls = map(lambda path: call(path, True), ASSERTED_FILE_PATHS)
        generalize_mock.assert_has_calls(calls)

    @patch('dotmgr.manager.symlink')
    @patch('dotmgr.manager.exists')
    def test_link_existing(self, exists_mock, symlink_mock):
        """Tests link with an already existing link.
        """
        exists_mock.return_value = True
        with patch('dotmgr.manager.home_path'):
            self.mgr.link(MOCKED_DOTFILE_PATH)
        self.assertFalse(symlink_mock.called)

    @patch('dotmgr.manager.home_path')
    @patch.object(Manager, 'stage_path')
    def test_link_new(self, stagepath_mock, homepath_mock):
        """Tests link.
        """
        destination_path = self.stage_file_path
        link_path = self.home_file_path
        homepath_mock.return_value = link_path
        self.exist_mock.return_value = False
        stagepath_mock.return_value = destination_path
        with patch('builtins.print'):
            self.mgr.link(MOCKED_DOTFILE_PATH)
        self.mkdir_mock.assert_called_once_with(dirname(link_path), exist_ok=True)
        self.ln_mock.assert_called_once_with(destination_path, link_path)

    @patch.object(Manager, 'link')
    def test_link_all(self, link_mock):
        """Tests link_all.
        """
        self.ls_mock.side_effect = MOCKED_FILE_LISTINGS
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False]
        with patch('builtins.print'):
            self.mgr.link_all()
        link_mock.assert_has_calls(map(call, ASSERTED_FILE_PATHS))

    def test_repo_path(self):
        """Tests repo_path.
        """
        self.assertEqual(self.repo_file_path, self.mgr.repo_path(MOCKED_DOTFILE_PATH))

    @patch.object(Manager, 'link')
    @patch.object(Transformer, 'specialize')
    def test_specialize(self, specialize_mock, link_mock):
        """Tests specializing a file.
        """
        mock_open(mock=self.open_mock, read_data='line1\nline2')
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH, False)
        self.mkdir_mock.assert_called_once_with(dirname(self.stage_file_path), exist_ok=True)
        specialize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.stage_file_path, 'w', encoding='utf-8')])
        self.assertFalse(link_mock.called)

    @patch.object(Manager, 'link')
    @patch.object(Transformer, 'specialize')
    def test_specialize_and_link(self, specialize_mock, link_mock):
        """Tests specializing and linking a file.
        """
        mock_open(mock=self.open_mock, read_data='line1\nline2')
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH, True)
        self.mkdir_mock.assert_called_once_with(dirname(self.stage_file_path), exist_ok=True)
        specialize_mock.assert_called_once_with(['line1\n', 'line2'])
        self.open_mock.assert_has_calls([call(self.stage_file_path, 'w', encoding='utf-8')])
        link_mock.assert_called_once_with(MOCKED_DOTFILE_PATH)

    @patch.object(Manager, 'link')
    @patch.object(Transformer, 'specialize')
    @patch.object(Transformer, 'parse_header')
    def test_specialize_skipped(self, parse_mock, specialize_mock, link_mock):
        """Tests specialize with a file that should be skipped.
        """
        parse_mock.return_value = {'skip': True}
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH, False)
        self.assertEqual(self.open_mock.call_count, 1)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(specialize_mock.called)
        self.assertFalse(link_mock.called)

    @patch.object(Manager, 'link')
    @patch.object(Transformer, 'specialize')
    def test_specialize_non_existing(self, specialize_mock, link_mock):
        """Tests specialize with a non-existing file.
        """
        self.open_mock.side_effect = FileNotFoundError
        with patch('builtins.print'):
            self.mgr.specialize(MOCKED_DOTFILE_PATH, False)
        self.assertFalse(self.mkdir_mock.called)
        self.assertFalse(specialize_mock.called)
        self.assertEqual(self.open_mock.call_count, 1)
        self.assertFalse(link_mock.called)

    @patch.object(Manager, 'link_all')
    @patch.object(Manager, 'specialize')
    def test_specialize_all(self, specialize_mock, link_mock):
        """Tests specialize_all.
        """
        file_listings = deepcopy(MOCKED_FILE_LISTINGS)
        file_listings[0].append('.git')
        file_listings[0].append('stage')
        file_listings[1].append('.git')
        file_listings.append(['file_on_stage'])
        self.ls_mock.side_effect = file_listings
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False, True, False]
        self.mgr.dotfile_stage_path = MOCKED_REPO_PATH + '/stage'
        with patch('builtins.print'):
            self.mgr.specialize_all(False)
        calls = map(lambda path: call(path, False), ASSERTED_FILE_PATHS)
        specialize_mock.assert_has_calls(calls)
        self.assertEqual(specialize_mock.call_count, len(ASSERTED_FILE_PATHS))
        self.assertFalse(link_mock.called)

    @patch.object(Manager, 'link_all')
    @patch.object(Manager, 'specialize')
    def test_specialize_all_and_link(self, specialize_mock, link_mock):
        """Tests specialize_all.
        """
        self.ls_mock.side_effect = MOCKED_FILE_LISTINGS
        self.isdir_mock.side_effect = [True, True, False, False, False, False, False]
        with patch('builtins.print'):
            self.mgr.specialize_all(True)
        calls = map(lambda path: call(path, True), ASSERTED_FILE_PATHS)
        specialize_mock.assert_has_calls(calls)
        self.assertEqual(specialize_mock.call_count, len(ASSERTED_FILE_PATHS))
        link_mock.assert_called_once_with()

    def test_stage_path(self):
        """Tests stage_path.
        """
        self.assertEqual(self.stage_file_path, self.mgr.stage_path(MOCKED_DOTFILE_PATH))

    def test_home_path(self):
        """Tests home_path.
        """
        self.assertEqual(self.home_file_path, home_path(MOCKED_DOTFILE_PATH))
