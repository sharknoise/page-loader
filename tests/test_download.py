import pytest

from page_load import core
from tests import conftest

TEMP_DIR = 'test_core_success'


def test_core_real_response(tmp_path):
    core.download_page(conftest.TEST_URL, tmp_path)
    saved_page = tmp_path / conftest.EXPECTED_PAGE_FILENAME
    assert saved_page.read_text() == conftest.FIXTURE_PAGE_PATH.read_text()


def test_core_success(mock_response200, tmp_path):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    core.download_page(conftest.TEST_URL, tmp_path)
    saved_page = tmp_path / conftest.EXPECTED_PAGE_FILENAME

    assert saved_page.exists(), (
        "Wrong page filename or the page wasn't saved."
    )

    assert saved_page.read_text() == conftest.FIXTURE_PAGE_PATH.read_text(), (
        'Content of the saved page is different.'
    )


def test_core_fail(mock_response404):
    with pytest.raises(ValueError):
        core.download_page(conftest.TEST_URL)
