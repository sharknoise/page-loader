from importlib import reload

import pytest
from page_load import core
from tests import conftest as ct

TEMP_DIR = 'success'


def test_mock_download_page(mock_response200, tmp_path):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    # to avoid incrementing names_counter for repeating filenames
    reload(core)
    core.download_page(ct.TEST_URL, destination)
    saved_page_path = destination / ct.SAVED_FIXTURE_FILENAME

    assert saved_page_path.exists(), (
        "Wrong page filename or the page wasn't saved."
    )

    assert (
        saved_page_path.read_text() == ct.SAVED_FIXTURE_PATH.read_text()
    ), ('Content of the saved page is different.')

    for saved_res, mock_res in zip(
        ct.SAVED_RESOURCE_PATHS, ct.MOCK_RESOURCE_PATHS,
    ):
        saved_res_path = destination / ct.SAVED_RESOURCE_DIR / saved_res
        mock_res_path = ct.FIXTURES_DIR / mock_res
        assert saved_res_path.read_bytes() == mock_res_path.read_bytes()


def test_real_download_page(tmp_path):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    # to avoid incrementing names_counter for repeating filenames
    reload(core)
    core.download_page(ct.TEST_URL, destination)
    saved_page_path = destination / ct.SAVED_FIXTURE_FILENAME

    assert saved_page_path.exists(), (
        "Wrong page filename or the page wasn't saved."
    )

    assert (
        saved_page_path.read_text() == ct.SAVED_FIXTURE_PATH.read_text()
    ), ('Content of the saved page is different.')

    for saved_res, mock_res in zip(
        ct.SAVED_RESOURCE_PATHS, ct.MOCK_RESOURCE_PATHS,
    ):
        saved_res_path = destination / ct.SAVED_RESOURCE_DIR / saved_res
        mock_res_path = ct.FIXTURES_DIR / mock_res
        assert saved_res_path.read_bytes() == mock_res_path.read_bytes()


@pytest.mark.parametrize('code', ct.ERROR_CODES, ids=ct.ERROR_IDS)
def test_download_page_http_error(mock, code):
    mock.get(ct.TEST_URL, status_code=code)
    with pytest.raises(core.PageLoadWebError):
        core.download_page(ct.TEST_URL)


def test_missing_schema():
    with pytest.raises(core.PageLoadWebError) as error_info:
        core.download_page(ct.URL_WITHOUT_SCHEMA)
    assert 'No schema supplied' in str(error_info.value)


def test_connection_error(mock_response_connection_error):
    with pytest.raises(core.PageLoadWebError) as error_info:
        core.download_page(ct.TEST_URL)
    assert 'Connection error' in str(error_info.value)


def test_response_timeout(mock_response_timeout):
    with pytest.raises(core.PageLoadWebError):
        core.download_page(ct.TEST_URL)


def test_many_redirects(mock_response_many_redirects):
    with pytest.raises(core.PageLoadWebError):
        core.download_page(ct.TEST_URL)
