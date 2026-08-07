import argparse
import sys

from jd_helper import index

ACTIONS = ["build-index"]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jdh")
    parser.add_argument("action", choices=ACTIONS)
    return parser


def main():
    parser = _parser()
    args = parser.parse_args(sys.argv[1:])
    if args.action == "build-index":
        index.build_index()
