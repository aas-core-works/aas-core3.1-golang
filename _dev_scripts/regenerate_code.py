"""Generate the SDK based on the aas-core-meta model and the snippets."""

import argparse
import os
import pathlib
import subprocess
import sys


def main() -> int:
    """Execute the main routine."""
    repo_root = pathlib.Path(os.path.realpath(__file__)).parent.parent

    default_meta_model_path = os.path.relpath(
        str(repo_root / "_dev_scripts" / "codegen" / "meta_model.py"),
        os.getcwd(),
    )

    default_snippet_dir = os.path.relpath(
        str(repo_root / "_dev_scripts" / "codegen" / "snippets"), os.getcwd()
    )

    default_output_dir = os.path.relpath(str(repo_root), os.getcwd())

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--meta_model", help="Path to the meta-model", default=default_meta_model_path
    )
    parser.add_argument(
        "--snippet_dir",
        help="Path to the directory containing implementation-specific snippets",
        default=default_snippet_dir,
    )
    parser.add_argument(
        "--output_dir",
        help="Path to the directory where the generated files are to be output",
        default=default_output_dir,
    )
    args = parser.parse_args()

    meta_model_path = pathlib.Path(args.meta_model)
    snippet_dir = pathlib.Path(args.snippet_dir)
    output_dir = pathlib.Path(args.output_dir)

    subprocess.run(
        [
            "aas-core-codegen",
            "--model_path",
            str(meta_model_path),
            "--snippets_dir",
            str(snippet_dir),
            "--output_dir",
            str(output_dir),
            "--target",
            "golang",
        ],
        check=True,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
