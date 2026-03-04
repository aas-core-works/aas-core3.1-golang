"""Update to the latest meta-model and the latest test data."""

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

    print("Downloading the latest meta-model...")
    subprocess.check_call(
        [
            sys.executable,
            str(repo_root / "_dev_scripts" / "download_aas_core_meta_model.py"),
        ],
        cwd=str(repo_root),
    )

    print("Generating the code...")
    subprocess.check_call(
        [
            sys.executable,
            str(repo_root / "_dev_scripts" / "regenerate_code.py"),
        ],
        cwd=str(repo_root),
    )

    print("Re-formatting the code...")
    subprocess.run(
        [sys.executable, str(repo_root / "_dev_scripts" / "reformat_code.py")],
        cwd=repo_root,
        check=True,
    )

    print("Downloading the latest test data...")
    subprocess.check_call(
        [
            sys.executable,
            str(repo_root / "_dev_scripts" / "download_latest_test_data.py"),
        ],
        cwd=str(repo_root),
    )

    print("Re-recording the test data...")
    subprocess.check_call(
        [sys.executable, str(repo_root / "_dev_scripts" / "rerecord_tests.py")],
        cwd=str(repo_root),
    )

    print("Running the pre-commit to check that everything worked...")
    subprocess.check_call(["go", "vet", "./..."], cwd=repo_root)

    env = os.environ.copy()
    env["GITHUB_COM_AAS_CORE_WORKS_AAS_CORE3_1_GOLANG_TEST_DATA_DIR"] = str(
        repo_root / "testdata"
    )

    subprocess.check_call(["go", "test", "./..."], cwd=repo_root, env=env)

    return 0


if __name__ == "__main__":
    sys.exit(main())
