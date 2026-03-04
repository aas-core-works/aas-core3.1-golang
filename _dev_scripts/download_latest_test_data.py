"""Download the latest test data released on aas-core-testdatagen."""

import argparse
import collections
import json
import os
import pathlib
import shutil
import sys
import uuid
import zipfile
from typing import Final

import requests
from icontract import require

_REPO: Final[str] = "aas-core-works/aas-core-testdatagen"


def _get_latest_version() -> str:
    """Get the latest version tag from aas-core-testdatagen GitHub repository."""
    url = f"https://api.github.com/repos/{_REPO}/releases/latest"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        tag_name = data.get("tag_name")

        if not isinstance(tag_name, str):
            raise RuntimeError(
                f"Expected the 'tag_name' to be a string, but got: {tag_name}"
            )

        return tag_name
    except (requests.RequestException, KeyError) as exception:
        raise RuntimeError(
            f"Error fetching the latest version from {url}"
        ) from exception


def _construct_download_url(version: str) -> str:
    """Construct the download URL for the test data zip file."""
    return (
        f"https://github.com/{_REPO}/releases/download/{version}/test_data_for_v3_1.zip"
    )


def _download(url: str, destination: pathlib.Path) -> None:
    """Download the test data zip file."""
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


# fmt: off
@require(
    lambda zip_path:
    zip_path.name.endswith(".zip")
    and zip_path.exists()
    and zip_path.is_file()
)
# fmt: on
def _extract_zip_in_its_parent(zip_path: pathlib.Path) -> None:
    """Extract the archive in its directory."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(zip_path.parent)

    except Exception as exception:
        raise RuntimeError(
            f"Failed to unpack {zip_path} to {zip_path.parent}"
        ) from exception


def main() -> int:
    """Execute the main routine."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.parse_args()

    repo_root = pathlib.Path(os.path.realpath(__file__)).parent.parent

    test_data_dir = repo_root / "testdata"

    json_dir = test_data_dir / "Json"
    if json_dir.exists():
        print(f"Deleting existing {json_dir} ...")
        shutil.rmtree(json_dir)

    xml_dir = test_data_dir / "Xml"
    if xml_dir.exists():
        print(f"Deleting existing {xml_dir} ...")
        shutil.rmtree(xml_dir)

    source_path = test_data_dir / "source.json"
    if source_path.exists():
        print(f"Deleting existing {source_path} ...")
        source_path.unlink()

    latest_version = _get_latest_version()
    if latest_version is None:
        print("Failed to get latest version")
        return 1

    print(f"Latest version: {latest_version}")

    url = _construct_download_url(latest_version)

    zip_path = test_data_dir / f"test_data_for_v3_1.{uuid.uuid4()}.zip"

    try:
        print(f"Downloading from: {url} to {zip_path} ...")
        _download(url=url, destination=zip_path)
        _extract_zip_in_its_parent(zip_path=zip_path)

        print(f"Writing the version to {source_path} ...")
        with source_path.open("wt") as fid:
            json.dump(
                collections.OrderedDict([("version", latest_version), ("url", url)]),
                fid,
                indent=2,
            )

    finally:
        print(f"Deleting {zip_path} ...")
        zip_path.unlink()

    return 0


if __name__ == "__main__":
    sys.exit(main())
