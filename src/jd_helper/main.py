import argparse
import sys


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jdh")
    return parser


def main():
    parser = _parser()
    parser.parse_args(sys.argv[1:])
