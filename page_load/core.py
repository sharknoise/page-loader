"""Core functions for page-loader."""

import collections
import logging
import re
import types
import urllib
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from progress.bar import FillingSquaresBar

SUCCESSFUL_STATUS_CODE = 200
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    +
    '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
)

EXTENSION = '.html'
SUFFIX = '_files'
IMPORTANT_TAGS = types.MappingProxyType({
    'link': 'href',
    'script': 'src',
    'img': 'src',
})
SCHEME = re.compile('^(http)s?(://)')

FILENAME_WITH_EXTENSION = re.compile(
    r'(?P<name>.+)(?P<extension>\.[a-zA-Z0-9]+$)',
)
NOT_LETTERS_OR_DIGITS = re.compile('[^a-zA-Zа-яА-Я0-9]')
SEPARATOR = '-'
MAX_FILENAME_LENGTH = 255

logger = logging.getLogger()

names_counter = collections.Counter()


class PageLoadError(Exception):
    """An error caught, logged and re-raised by page_load.core."""

    pass  # noqa: WPS420, WPS604


class PageLoadWebError(PageLoadError):
    """An error caught, logged and re-raised by download_page."""

    pass  # noqa: WPS420, WPS604


class PageLoadWriteError(PageLoadError):
    """An error caught, logged, re-raised by write_to_file, make_directory."""

    pass  # noqa: WPS420, WPS604


def download_page(target_url, destination=''):  # noqa: WPS231  # complexity
    """
    Download a web page to a local directory.

    Args:
        target_url: url of the page
        destination: directory to store the page

    Raises:
        PageLoadWebError: an error while requesting the page
    """
    path = Path(destination)

    try:
        page_content, page_binary, response_url = send_request(target_url)
    except requests.exceptions.ConnectionError as wrong_url_error:
        raise PageLoadWebError(
            'Connection error, check whether the URL is correct.',
        ) from wrong_url_error
    except (
        requests.HTTPError,
        requests.exceptions.MissingSchema,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
    ) as page_request_error:
        raise PageLoadWebError(
            str(page_request_error),
        ) from page_request_error

    prepared = parse_and_process_page(page_content, response_url)
    page, page_filename, resources = prepared

    saved_page_path = write_to_file(
        path / page_filename,
        page,
        binary_mode=page_binary,
    )

    if resources:
        download_resources(resources, path)

    if saved_page_path:
        logging.info('Saved as {0}'.format(saved_page_path))


def download_resources(resources, path):
    """
    Download page resources to the specified directory.

    Show the download progress in terminal.

    Args:
        resources: list of (url, local storage subpath) tuples
        path: parent directory for local storage
    """
    download_progress = FillingSquaresBar(
        'Downloading page resources',
        max=len(resources),
        suffix='%(percent)d%%',  # noqa:WPS323
    )
    for resource_url, resource_filename in resources:
        logging.debug(
            'resource_url: {0}, resource_filename: {1}'.format(
                resource_url, resource_filename,
            ),
        )
        try:
            resource_content, resource_binary, _ = send_request(
                resource_url,
            )
        except Exception as resource_request_error:
            logging.warning(
                'Resource download failed: {0}'.format(
                    str(resource_request_error),
                ),
                exc_info=logger.isEnabledFor(logging.DEBUG),
            )
            continue

        write_to_file(
            path / resource_filename,
            resource_content,
            binary_mode=resource_binary,
        )
        download_progress.next()  # noqa: B305

    download_progress.finish()


def send_request(url):
    """
    Send request to the specified url.

    Args:
        url: url of the page or a resource

    Returns:
        A tuple of three values
        response_content: content of the response
        binary: true if the content is binary
        response.url
    """
    headers = {'User-Agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    # raises HTTPError if one occured
    response.raise_for_status()

    if response.encoding:
        response_content = response.text
        binary = False
    else:
        response_content = response.content
        binary = True

    return (response_content, binary, response.url)


def parse_and_process_page(decoded_html, url):
    """
    Send request to the specified url.

    Args:
        decoded_html: html content from the response
        url: original location of the page

    Returns:
        A tuple of three values
        soup as a string
        page_filename to store the page locally
        resources: a list of page resources
    """
    soup = BeautifulSoup(decoded_html, features='html.parser')

    base_for_name = make_name_from_url(url)
    page_filename = base_for_name + EXTENSION
    resources_dir = Path(base_for_name + SUFFIX)

    resources = []
    tags_with_resources = soup.find_all(IMPORTANT_TAGS.keys())
    page_domain = re.compile(urllib.parse.urlparse(url).netloc)

    for tag in tags_with_resources:
        attr_val = tag.get(IMPORTANT_TAGS[tag.name])
        if attr_val is None:
            logging.debug(
                'Important tag has no src or href:\n {0}'.format(tag),
            )
            continue
        if SCHEME.search(attr_val) is None or page_domain.search(attr_val):
            attribute_name = IMPORTANT_TAGS[tag.name]
            resource_url = urllib.parse.urljoin(
                url,
                tag[attribute_name],
            )

            resource_filename = resources_dir / make_name_from_url(
                tag[attribute_name],
                search_extension=True,
            )
            resources.append((resource_url, resource_filename))
            new_value = resource_filename
            tag[attribute_name] = new_value

    return (str(soup), page_filename, resources)


def make_name_from_url(url, search_extension=False):
    """
    Substitute symbols in a URL to make a valid filename for local storage.

    Args:
        url: url of a page or a resource
        search_extension: set to True for images and other resources

    Returns:
        valid filename as a string
    """
    parsed_url = urllib.parse.urlparse(urllib.parse.unquote(url))
    url_without_scheme = parsed_url.netloc + parsed_url.path
    # if the url starts or ends with a slash, remove the slash
    cleared_url = re.sub('^/|/$', '', url_without_scheme)

    if search_extension:
        parts = FILENAME_WITH_EXTENSION.search(cleared_url)
        if parts is not None:
            short_name = make_short_name(
                NOT_LETTERS_OR_DIGITS.sub(SEPARATOR, parts.group('name')),
                parts.group('extension'),
            )
            if short_name:
                return short_name

    return make_short_name(
        NOT_LETTERS_OR_DIGITS.sub(SEPARATOR, cleared_url),
        '',
    )


def make_short_name(name, extension):
    """
    Shorten a filename to an acceptable length, taking encoding into account.

    Args:
        name: filename to shorten
        extension: extension of the file

    Returns:
        filename shortened to MAX_FILENAME_LENGTH
    """
    result_name = ''

    name_bytes = name.encode()
    extension_bytes = extension.encode()

    if len(extension_bytes) >= MAX_FILENAME_LENGTH:
        return result_name

    length = MAX_FILENAME_LENGTH - len(extension_bytes)
    expected_name = name_bytes[:length] + extension_bytes

    filename_number = names_counter[expected_name]

    if filename_number == 0:
        result_name = expected_name.decode(errors='ignore')
    else:
        filename_number_bytes = str(filename_number).encode()
        length -= len(filename_number_bytes)
        if length <= 0:
            return result_name
        result_name = (
            name_bytes[:length] + filename_number_bytes + extension_bytes
        ).decode(errors='ignore')

    names_counter[expected_name] += 1
    return result_name


def write_to_file(path_to_file, data_to_write, binary_mode=False):
    """Write data to a file, using binary mode if necessary."""
    full_path = Path().absolute() / Path(path_to_file)
    make_directory(full_path)
    logging.debug('Saving {0}'.format(full_path))

    try:
        with open(full_path, 'wb' if binary_mode else 'w') as target_file:
            target_file.write(data_to_write)
    except OSError as file_writing_error:
        raise PageLoadWriteError(
            str(file_writing_error),
        ) from file_writing_error
    return full_path


def make_directory(path_to_file):
    """Create a parent directory for a file based on the specified path."""
    path = Path(path_to_file)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as directory_writing_error:
        raise PageLoadWriteError(
            str(directory_writing_error),
        ) from directory_writing_error
