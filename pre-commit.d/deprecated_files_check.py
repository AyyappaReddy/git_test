#!/usr/bin/env python3

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel


class DeprecationNotice(BaseModel):
    name: str
    """Name of the deprecation"""

    regex: str
    """Regex to match the files to"""

    message: str
    """The Deprecation Notice message"""


class DeprecationsConfig(BaseModel):
    deprecations: Optional[List[DeprecationNotice]]
    """List of Deprecation Notices"""


def load_deprecations_config(deprecation_file: Path) -> DeprecationsConfig:
    """Load the deprecations config file"""
    try:
        with deprecation_file.open("r") as f:
            return DeprecationsConfig(**yaml.safe_load(f))
    except IOError as io_error:
        logging.error(f"Could not load config. {io_error}")
        sys.exit(1)
    except TypeError as type_error:
        logging.error(f"Error in config {deprecation_file}. {type_error}")
        sys.exit(1)
    except KeyError as key_error:
        logging.error(f"Error in config {deprecation_file}: Missing key {key_error}.")
        sys.exit(1)


def main():
    """Check if any of the arguments is in the deprecated file list. The config is passed as the first argument."""
    logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)d] %(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("filenames", type=str, nargs="+", help="File names to be checked.")
    parser.add_argument(
        "--config",
        required=False,
        type=Path,
        default=Path(__file__).parent / "deprecated_files_check.yaml",
        help="The configuration file with the deprecations list",
    )
    args = parser.parse_args()
    config = load_deprecations_config(args.config)

    failures = 0
    for changed_file in args.filenames:
        for deprecation in config.deprecations:
            rematch = re.match(deprecation.regex, changed_file)
            if rematch:
                prettier_message = "\n| ".join(deprecation.message.splitlines())
                logging.error((f"Deprecation match: {deprecation.name}\n" f'+{"-"*80}\n' f"| {prettier_message}\n|"))
                failures += 1

    if failures > 0:
        logging.error(
            (
                f"{failures} deprecated file{'s' if failures >= 2 else ''} modified.\n"
                " - If you really need to make a change use SKIP='changes-in-deprecated-files' to skip this check.\n"
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
