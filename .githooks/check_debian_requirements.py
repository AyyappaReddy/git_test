#!/usr/bin/env python3
"""Check if all required debian packages are installed for pre-commit hooks."""
__copyright__ = """
@copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""

import click
import subprocess
import sys


@click.command()
def main():
    """Test that each required package is available in the right version."""

    # return on windows and macos; this check is impossible
    if sys.platform in ["win32", "darwin"]:
        return 0

    # list of tuples of debian packages to check
    #   Format: (name, min_version)
    debians = [("athena-clang-tools-1", "1.1.0")]

    # error list
    errors = []

    # check each debian package
    for name, min_version in debians:
        cmd = "dpkg-query -f=${Version} --show " + f"{name}"
        output = subprocess.run(cmd.split(), encoding="utf-8", stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if not output.returncode:
            actual_version = output.stdout
            cmd = f"dpkg --compare-versions {actual_version} ge {min_version}"
            output = subprocess.run(cmd.split())
            if output.returncode:
                errors.append(
                    f"{name} found in wrong version.  actual version == {actual_version}; minimum version == {min_version}"
                )
        else:
            errors.append(f"{name} not installed.")

    if errors:
        print("pre-commit debian version errors:", *errors, sep="\n- ")
        sys.exit(2)


if __name__ == "__main__":
    main()
