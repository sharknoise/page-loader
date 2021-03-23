import pytest

from page_load import core
from tests import conftest


def test_core_real_response(tmp_path):
    core.download_page(conftest.TEST_URL, tmp_path)
    saved_page = tmp_path / conftest.EXPECTED_PAGE_FILENAME
    assert saved_page.read_text() == conftest.FIXTURE_PAGE_PATH.read_text()


def test_core_success(mock_response200, tmp_path):
    core.download_page(conftest.TEST_URL, tmp_path)
    saved_page = tmp_path / conftest.EXPECTED_PAGE_FILENAME
    assert saved_page.read_text() == conftest.FIXTURE_PAGE_PATH.read_text()


def test_core_fail(mock_response404):
    with pytest.raises(ValueError):
        core.download_page(conftest.TEST_URL)
