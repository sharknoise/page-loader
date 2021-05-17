"""Command line parser for page-loader."""

import argparse

parser = argparse.ArgumentParser(description='Page-loader')

parser.add_argument(
    'target_url',
    help='URL of the page',
    )

parser.add_argument(
    '-o',
    '--output',
    help='set the save directory',
    metavar='OUTPUT',
    dest='destination',
    default='',
)

parser.add_argument(
    '-l',
    '--log',
    help=(
        "set logging level: 'none', 'info', 'warning', 'debug'"
    ),
    metavar='LOG_LEVEL',
    dest='log_level',
    choices=['none', 'info', 'warning', 'debug'],
    default='info',
)
