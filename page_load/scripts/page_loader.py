"""A script to run page-loader in terminal."""

import logging
import sys

from page_load.cli import parser
from page_load.core import (
    PageLoadError,
    PageLoadWebError,
    PageLoadWriteError,
    download_page,
)
from page_load.logging import setup

SUCCESSFUL_EXIT_CODE = 0
COMMON_ERROR_EXIT_CODE = 1
WEB_ERROR_EXIT_CODE = 2
WRITE_ERROR_EXIT_CODE = 3


def main():
    """Run the utility in terminal."""
    arguments = parser.parse_args()
    setup(arguments.log_level)
    try:
        download_page(
            arguments.target_url,
            destination=arguments.destination,
        )
    except PageLoadError as known_error:
        logging.error(str(known_error))
        logging.debug(str(known_error), exc_info=True)
        if isinstance(known_error, PageLoadWebError):
            sys.exit(WEB_ERROR_EXIT_CODE)
        elif isinstance(known_error, PageLoadWriteError):
            sys.exit(WRITE_ERROR_EXIT_CODE)
        else:
            sys.exit(COMMON_ERROR_EXIT_CODE)
    sys.exit(SUCCESSFUL_EXIT_CODE)


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
