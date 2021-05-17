"""A script to run page-loader in terminal."""

from page_load.cli import parser
from page_load.core import download_page
from page_load.logging import setup


def main():
    """Run the utility in terminal."""
    arguments = parser.parse_args()
    setup(arguments.log_level)
    download_page(
        arguments.target_url,
        destination=arguments.destination,
    )


# Check if the module runs as a program.
if __name__ == '__main__':
    main()
