#!/usr/bin/env python3

__doc__ = """
This script checks file name against the file name rules.

To be called with (relative) file paths as command line arguments.

Example:

    filename_checker.py documentation/conf.py documentation/README.md

The script exits with an error log message if a file name violates one of rules listed below.
"""

__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""
import logging
import sys
from typing import List


def main(args: List[str]) -> bool:
    """Check every filename in args if it adheres to the following filename rules:

    - only contains letters, numbers, or any of the following characters: ``./_+-``

    It prints a warning for every wrong file name in the list,
    so that users only have to run the hook a single time to see all required fixes.

    Args:
        args (List[str]): list of strings containing relative file paths, like "documentation/conf.py"

    Returns:
        bool: True if all file paths in args are valid, False otherwise
    """
    all_ok = True
    logging.basicConfig(level=logging.INFO, format="[%(filename)s:%(lineno)d] %(levelname)s: %(message)s")

    class MarkInvalidChars:
        """Replace invalid chars by carets and valid chars by spaces."""

        @staticmethod
        def __getitem__(c):
            c = chr(c)
            # We need to include the path separator / because we get relative paths as input.
            if "a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c in "/_+.-":
                return " "
            return "^"

    for filename in args:
        markers = filename.translate(MarkInvalidChars())
        # whitespaces are removed by strip(), so if anything remains, it's an invalid character marker:
        if markers.strip():
            all_ok = False
            logging.error(f"File path contains forbidden character(s):\n  {filename}\n  {markers.rstrip()}")

    return all_ok


if __name__ == "__main__":
    if main(sys.argv[1:]) is False:
        sys.exit(1)
