"""Tests for the paths module.
"""
from os import environ
from os.path import expanduser
from unittest import TestCase
from unittest.mock import patch

from dotmgr.paths import (DEFAULT_DOTFILE_REPOSITORY_PATH,
                          DEFAULT_DOTFILE_STAGE_PATH,
                          DEFAULT_DOTFILE_TAG_CONFIG_PATH,
                          REPOSITORY_PATH_VAR,
                          STAGE_PATH_VAR,
                          TAG_CONFIG_PATH_VAR,
                          prepare_dotfile_repository_path,
                          prepare_dotfile_stage_path,
                          prepare_tag_config_path)

MOCKED_REPO_PATH = '/tmp/repository'
MOCKED_STAGE_PATH = '/tmp/stage'
MOCKED_TAG_CONFIG_PATH = '/tmp/tags.conf'

class PathsTest(TestCase):
    """Tests for the paths module.
    """

    def test_repo_path_default(self):
        """Tests prepare_dotfile_repository_path when DOTMGR_REPO is not defined.
        """
        self.assertEqual(prepare_dotfile_repository_path(False, False),
                         expanduser(DEFAULT_DOTFILE_REPOSITORY_PATH))

    @patch.dict(environ, {REPOSITORY_PATH_VAR:MOCKED_REPO_PATH})
    def test_repo_path_from_env(self):
        """Tests prepare_dotfile_repository_path when DOTMGR_REPO is defined in the environment.
        """
        self.assertEqual(prepare_dotfile_repository_path(False, False), MOCKED_REPO_PATH)

    @patch('dotmgr.paths.isdir')
    def test_repo_path_verify(self, isdir_mock):
        """Tests prepare_dotfile_repository_path with verification when DOTMGR_REPO is not defined.
        """
        isdir_mock.return_value = True
        self.assertEqual(prepare_dotfile_repository_path(True, False),
                         expanduser(DEFAULT_DOTFILE_REPOSITORY_PATH))

    @patch('dotmgr.paths.isdir')
    @patch.dict(environ, {REPOSITORY_PATH_VAR:MOCKED_REPO_PATH})
    def test_repo_path_from_env_verify(self, isdir_mock):
        """Tests prepare_dotfile_repository_path with verification when DOTMGR_REPO is defined in
           the environment.
        """
        isdir_mock.return_value = True
        self.assertEqual(prepare_dotfile_repository_path(False, False), MOCKED_REPO_PATH)

    @patch('dotmgr.paths.isdir')
    def test_repo_path_error(self, isdir_mock):
        """Tests prepare_dotfile_repository_path with failing verification.
        """
        isdir_mock.return_value = False
        with patch('builtins.print'), self.assertRaises(SystemExit):
            prepare_dotfile_repository_path(True, False)

    def test_stage_path_default(self):
        """Tests prepare_dotfile_stage_path when DOTMGR_STAGE is not defined.
        """
        self.assertEqual(prepare_dotfile_stage_path(False),
                         expanduser(DEFAULT_DOTFILE_STAGE_PATH))

    @patch.dict(environ, {STAGE_PATH_VAR:MOCKED_STAGE_PATH})
    @patch('dotmgr.paths.isdir')
    def test_stage_path_from_env(self, isdir_mock):
        """Tests prepare_dotfile_stage_path when DOTMGR_STAGE is defined in the environment and
           the directory is present.
        """
        isdir_mock.return_value = True
        self.assertEqual(prepare_dotfile_stage_path(False), MOCKED_STAGE_PATH)

    @patch.dict(environ, {STAGE_PATH_VAR:MOCKED_STAGE_PATH})
    @patch('dotmgr.paths.isdir')
    @patch('dotmgr.paths.makedirs')
    def test_stage_path_creation(self, makedirs_mock, isdir_mock):
        """Tests prepare_dotfile_stage_path when DOTMGR_STAGE is defined in the environment and
           the directory is not yet present.
        """
        isdir_mock.return_value = False
        self.assertEqual(prepare_dotfile_stage_path(False), MOCKED_STAGE_PATH)
        makedirs_mock.assert_called_once_with(MOCKED_STAGE_PATH)

    def test_config_path_default(self):
        """Tests prepare_dotfile_stage_path when DOTMGR_TAG_CONF is not defined.
        """
        self.assertEqual(prepare_tag_config_path(False, None, False, False),
                         '{}/{}'.format(environ['HOME'], DEFAULT_DOTFILE_TAG_CONFIG_PATH))

    @patch.dict(environ, {TAG_CONFIG_PATH_VAR:MOCKED_TAG_CONFIG_PATH})
    def test_config_path_from_env(self):
        """Tests prepare_tag_config_path when DOTMGR_TAG_CONF is defined in the environment.
        """
        self.assertEqual(prepare_tag_config_path(False, None, False, False), MOCKED_TAG_CONFIG_PATH)

    def test_config_path_bstrp_error(self):
        """Tests prepare_dotfile_stage_path in bootstrap mode without repository path.
        """
        with self.assertRaises(AssertionError):
            prepare_tag_config_path(True, None, False, False)

    def test_config_path_bootstrap(self):
        """Tests prepare_dotfile_stage_path in bootstrap mode with a valid repository path.
        """
        self.assertEqual(prepare_tag_config_path(True, MOCKED_REPO_PATH, False, False),
                         '{}/{}'.format(MOCKED_REPO_PATH, DEFAULT_DOTFILE_TAG_CONFIG_PATH))

    @patch('dotmgr.paths.isfile')
    def test_config_path_verify(self, isfile_mock):
        """Tests prepare_dotfile_stage_path in verifying mode with a non-existing config file.
        """
        isfile_mock.return_value = False
        with patch('builtins.print'), self.assertRaises(SystemExit):
            self.assertEqual(prepare_tag_config_path(False, None, True, False),
                             '{}/{}'.format(environ['HOME'], DEFAULT_DOTFILE_TAG_CONFIG_PATH))
