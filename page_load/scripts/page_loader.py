"""A script to run page-loader in terminal."""

import sys

from page_load.cli import parser
from page_load.core import PageLoadError, download_page
from page_load.logging import setup


def main():
    """Run the utility in terminal."""
    arguments = parser.parse_args()
    setup(arguments.log_level)
    try:
        download_page(
            arguments.target_url,
            destination=arguments.destination,
        )
    except PageLoadError:
        sys.exit(1)


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
