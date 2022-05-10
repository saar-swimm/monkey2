import os

import pytest
from tests.utils import add_files_to_dir, add_subdirs_to_dir

from common.utils.file_utils import (
    InvalidPath,
    expand_path,
    get_all_regular_files_in_directory,
    get_file_sha256_hash,
)


def test_expand_user(patched_home_env):
    input_path = os.path.join("~", "test")
    expected_path = patched_home_env / "test"

    assert expand_path(input_path) == expected_path


def test_expand_vars(patched_home_env):
    input_path = os.path.join("$HOME", "test")
    expected_path = patched_home_env / "test"

    assert expand_path(input_path) == expected_path


def test_expand_path__empty_path_provided():
    with pytest.raises(InvalidPath):
        expand_path("")


def test_get_file_sha256_hash(stable_file, stable_file_sha256_hash):
    assert get_file_sha256_hash(stable_file) == stable_file_sha256_hash


SUBDIRS = ["subdir1", "subdir2"]
FILES = ["file.jpg.zip", "file.xyz", "1.tar", "2.tgz", "2.png", "2.mpg"]


def test_get_all_regular_files_in_directory__no_files(tmp_path, monkeypatch):
    add_subdirs_to_dir(tmp_path, SUBDIRS)

    expected_return_value = []
    assert list(get_all_regular_files_in_directory(tmp_path)) == expected_return_value


def test_get_all_regular_files_in_directory__has_files(tmp_path, monkeypatch):
    add_subdirs_to_dir(tmp_path, SUBDIRS)
    files = add_files_to_dir(tmp_path, FILES)

    expected_return_value = sorted(files)
    assert sorted(get_all_regular_files_in_directory(tmp_path)) == expected_return_value


def test_get_all_regular_files_in_directory__subdir_has_files(tmp_path, monkeypatch):
    subdirs = add_subdirs_to_dir(tmp_path, SUBDIRS)
    add_files_to_dir(subdirs[0], FILES)

    files = add_files_to_dir(tmp_path, FILES)

    expected_return_value = sorted(files)
    assert sorted(get_all_regular_files_in_directory(tmp_path)) == expected_return_value
