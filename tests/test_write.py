import os
from importlib import reload

import pytest
from page_load import core
from tests import conftest as ct

FORBIDDEN_DIR = 'forbidden_dir'
READ_ONLY_CODE = 0o400


def test_not_a_directory(mock_response200, tmp_path):
    # to avoid incrementing names_counter for repeating filenames
    reload(core)

    with pytest.raises(core.PageLoadWriteError):
        core.download_page(ct.TEST_URL, ct.MOCK_FIXTURE_PATH)


def test_directory_permission_denied(mock_response200, tmp_path):
    # to avoid incrementing names_counter for repeating filenames
    reload(core)

    destination = tmp_path / FORBIDDEN_DIR
    destination.mkdir()
    os.chmod(destination, READ_ONLY_CODE)
    with pytest.raises(core.PageLoadWriteError) as error_info:
        core.download_page(ct.TEST_URL, destination)
    assert 'Permission denied' in str(error_info.value)
