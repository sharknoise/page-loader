"""Command line parser for page-loader."""

import argparse

parser = argparse.ArgumentParser(description='Page-loader')

parser.add_argument(
    'target_url',
    help='URL of the page',
    )

parser.add_argument(
    '--output',
    help=(
        'set the save directory',
    ),
    dest='destination',
)
