import logging
import os
import sys
from pathlib import Path

from jd_helper import application

logger = logging.getLogger()

JD_ROOT = Path("~/jd").expanduser()
# JDEX_ROOT = Path("~/jdex").expanduser()


def _setup_logging(normally_quiet=True):
    if "VERBOSE" in os.environ:
        log_level = logging.DEBUG
    elif normally_quiet:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")


def jdi():
    """Print the index (command line). This is the 'jdi' script."""
    _setup_logging()
    selected: str | None = None
    if len(sys.argv) > 1:
        selected = sys.argv[1]
    application.print_index_to_console(jd_root=JD_ROOT, selected=selected)
