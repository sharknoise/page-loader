from page_load import core
from tests import conftest


def test_core(tmp_path, test_page):
    core.download_page(conftest.TEST_URL, tmp_path)
    saved_page = tmp_path / conftest.TEST_PAGE_FILENAME
    assert saved_page.read_text() == conftest.TEST_PAGE_PATH.read_text()