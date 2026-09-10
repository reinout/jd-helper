import argparse
import logging
import os
import sys
from pathlib import Path

from jd_helper import application

logger = logging.getLogger()

JD_ROOT = Path("~/jd").expanduser()


def _setup_logging(normally_quiet=True):
    if "VERBOSE" in os.environ:
        log_level = logging.DEBUG
    elif normally_quiet:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")


def jdi():
    """Show the TUI with the index. This is the 'jdi' script."""
    _setup_logging()
    application.show_index(jd_root=JD_ROOT)


def jdcd():
    """cd into area, category or id, this is the 'jdcd' script."""
    _setup_logging()
    parser = argparse.ArgumentParser(prog="jdcd")
    parser.add_argument("number")
    args = parser.parse_args(sys.argv[1:])
    application.print_cd_into_dir(jd_root=JD_ROOT, number=args.number)


def jdh():
    """Print the full html output, this is the 'jdh' script."""
    _setup_logging()
    application.export_html_pages(jd_root=JD_ROOT)
