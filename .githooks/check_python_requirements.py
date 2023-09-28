#!/usr/bin/env python3
"""Check if all required pip tools are installed for pre-commit hooks."""


__copyright__ = """
@copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

The reproduction, distribution and utilization of this file as
well as the communication of its contents to others without express
authorization is prohibited. Offenders will be held liable for the
payment of damages and can be prosecuted. All rights reserved
particularly in the event of the grant of a patent, utility model
or design.
"""
import sys
from pathlib import Path
from typing import List, Tuple

import click
import yaml
from pkg_resources import DistributionNotFound, VersionConflict, require


def test_package_require(req: str) -> Tuple[bool, str]:
    """Returns errors in loading dependencies."""

    try:
        require(req)
    except DistributionNotFound:
        return False, f"{req} not found."
    except VersionConflict as err:
        req_parts = req.split("==")
        if len(req_parts) == 2:
            return False, f"{req_parts[0]} found in wrong version. {err}"
    return True, f"{req} found."


@click.command()
@click.argument("packages", nargs=-1, type=str)
def main(packages: List[str]):
    """Test that each required package is available in the right version."""

    with (Path(__file__).absolute().parent.parent / "tools/athenadep/aliases/aliases.yaml").open() as fin:
        python_deps = yaml.safe_load(fin)

    errors = []
    for item in packages:
        if f"pip3-{item}" in python_deps:
            req = python_deps[f"pip3-{item}"]["ubuntu"]["pip"]
            retval, msg = test_package_require(req)
            if not retval:
                errors.append(msg)
        else:
            errors.append(f"Could not find {item} in athenadep.")

    if errors:
        print("pre-commit python version errors:", *errors, sep="\n- ")
        sys.exit(2)


if __name__ == "__main__":
    main()
