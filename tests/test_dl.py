
import pytest
import requests

from page_load import core

TEMP_DIR = 'test_core_successful_response'


def test_core_successful_response(
    tmp_path,
    mock_response_successful,
    test_page,
):

    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    core.download_page(test_page['url'], destination)
    saved_page = destination / test_page['filename']

    assert saved_page.exists(), 'Wrong filename or page was not saved.'
    assert saved_page.read_text() == test_page['content'], (
        'Content of the saved page is different.'
    )


def test_core_error_response(mock_response_error, test_page):
    with pytest.raises(ValueError):
        core.download_page(test_page['url'])
