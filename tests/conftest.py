
from pathlib import Path

import pytest
import requests_mock

from page_load import logging

TESTS_DIR = Path(__file__).parent.absolute()
FIXTURES_DIR = TESTS_DIR / 'fixtures'
TEST_URL = 'http://sharknoise.github.io/pltest/'
MOCK_FIXTURE_FILENAME = 'mock_page.html'
MOCK_FIXTURE_PATH = FIXTURES_DIR / MOCK_FIXTURE_FILENAME
MOCK_RESOURCE_PATHS = (
    FIXTURES_DIR / 'resources/test_image1.jpg',
    FIXTURES_DIR / 'test_image2.png',
    FIXTURES_DIR / 'style.css',
)
SAVED_FIXTURE_FILENAME = 'sharknoise-github-io-pltest.html'
SAVED_FIXTURE_PATH = FIXTURES_DIR / SAVED_FIXTURE_FILENAME
SAVED_RESOURCE_DIR = 'sharknoise-github-io-pltest_files'
SAVED_RESOURCE_PATHS = (
    'resources-test-image1.jpg',
    'test-image2.png',
    'sharknoise-github-io-resources-style.css',
)
ERROR_CODES = (400, 401, 403, 404, 500)
ERROR_IDS = (
    'bad request', 'unauthorized', 'no privileges', 'not found', 'server error'
)
URL_WITHOUT_SCHEMA = 'wrong.com'


@pytest.fixture(scope='session', autouse=True)
def show_debug_messages():
    logging.setup(logging.DEBUG)


@pytest.fixture()
def mock():
    with requests_mock.Mocker(real_http=True) as m:
        yield m


@pytest.fixture
def mock_response200(mock):
    mock.register_uri(
        'GET',
        TEST_URL,
        text=MOCK_FIXTURE_PATH.read_text(),
    )
    path = FIXTURES_DIR / 'style.css'
    mock.register_uri(
        'GET',
        'http://sharknoise.github.io/resources/style.css',
        content=path.read_bytes(),
    )


@pytest.fixture
def mock_response404(mock):
    mock.register_uri(
        'GET', 
        TEST_URL,
        status_code=404,
    )
