"""Core functions for page-loader."""

import re
from pathlib import Path

import requests

MESSAGE_TEMPLATE = 'Download failed! Response code {code}'


def download_page(target_url, destination=None):
    """
    Download a web page to a local directory.

    Args:
        target_url: url of the page
        destination: directory to store the page

    Raises:
        ValueError: in case of bad request
    """
    request = requests.get(target_url)

    if request.ok:
        filename = make_filename(target_url)

        if destination is None:
            path = Path.cwd()
        else:
            path = Path(destination)

        with open(path / filename, 'w') as output_file:
            output_file.write(request.text)
    else:
        raise ValueError(
            MESSAGE_TEMPLATE.format(code=request.status_code),
        )


SCHEME = r'^.*//'
NOT_LETTERS_OR_DIGITS = r'[^a-zA-Z0-9]'
SEPARATOR = '-'
EXTENSION = '.html'


def make_filename(target_url):
    """
    Transform the url into a filename for local storage.

    Args:
        target_url: url of the page

    Returns:
        a valid filename string
    """
    url_without_scheme = re.sub(SCHEME, '', target_url)
    filename_without_extension = re.sub(
        NOT_LETTERS_OR_DIGITS,
        SEPARATOR,
        url_without_scheme,
    )
    return filename_without_extension + EXTENSION
