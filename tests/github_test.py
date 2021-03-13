from page_load import core

REAL_TEST_URL = 'http://sharknoise.github.io/index.html'
EXPECTED_FILENAME = 'sharknoise-github-io-index.html'
EXPECTED_HTML = "<img src='/test_image.jpg'>\n"


def test_core(tmp_path):
    core.download_page(REAL_TEST_URL, tmp_path)
    saved_page = tmp_path / EXPECTED_FILENAME
    assert saved_page.read_text() == EXPECTED_HTML
