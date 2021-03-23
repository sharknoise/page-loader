
from pathlib import Path

import pytest
import requests_mock

TESTS_DIR = Path(__file__).parent.absolute()
FIXTURES_DIR = TESTS_DIR / 'fixtures'
TEST_URL = 'http://sharknoise.github.io/index.html'
EXPECTED_PAGE_FILENAME = 'sharknoise-github-io-index.html'
FIXTURE_PAGE_PATH = FIXTURES_DIR / EXPECTED_PAGE_FILENAME


@pytest.fixture()
def mock():
    with requests_mock.Mocker(real_http=True) as m:
        yield m


@pytest.fixture
def mock_response200(mock):
    mock.register_uri(
        'GET',
        TEST_URL,
        text=FIXTURE_PAGE_PATH.read_text(),
    )


@pytest.fixture
def mock_response404(mock):
    mock.register_uri(
        'GET', 
        TEST_URL,
        status_code=404,
    )
