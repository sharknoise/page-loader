import pytest

from page_load import core
from tests import conftest

TEMP_DIR = 'success'


def test_core_real_response(tmp_path):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    core.download_page(conftest.TEST_URL, destination)
    saved_page_path = destination / conftest.EXPECTED_PAGE_FILENAME

    assert saved_page_path.exists(), (
        "Wrong page filename or the page wasn't saved."
    )

    assert saved_page_path.read_text() == conftest.FIXTURE_PAGE_PATH.read_text(), (
        'Content of the saved page is different.'
    )


def test_core_mock_success(mock_response200, tmp_path):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    core.download_page(conftest.TEST_URL, destination)
    saved_page_path = destination / conftest.EXPECTED_PAGE_FILENAME

    assert saved_page_path.exists(), (
        "Wrong page filename or the page wasn't saved."
    )

    assert saved_page_path.read_text() == conftest.FIXTURE_PAGE_PATH.read_text(), (
        'Content of the saved page is different.'
    )


def test_core_mock_fail(mock_response404):
    with pytest.raises(ValueError):
        core.download_page(conftest.TEST_URL)
