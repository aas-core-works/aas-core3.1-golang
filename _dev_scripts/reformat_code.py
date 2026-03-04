"""Reformat all the Golang files."""

import argparse
import os
import pathlib
import subprocess
import sys


def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.parse_args()

    repo_root = pathlib.Path(os.path.realpath(__file__)).parent.parent

    format_targets = sorted(
        str(path)
        for path in repo_root.glob("**/*.go")
        if not any(part.startswith("_") or part.startswith(".") for part in path.parts)
    )
    subprocess.run(
        ["gofmt", "-l", "-w", "-s"] + format_targets, cwd=repo_root, check=True
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
