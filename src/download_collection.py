#!/usr/bin/env python3
import csv
import logging
import time
from pathlib import Path

import click

from file_downloader import download_urls

logger = logging.getLogger(__name__)

S3 = "https://files.planning.data.gov.uk/"
COLLECTION_FILES = [
    "endpoint.csv",
    "source.csv",
    "log.csv",
    "resource.csv",
    "old-resource.csv",
]


def build_url_map(specification_dir="specification", timestamp=None):
    """Build {url: output_path} for every collection's collection files."""
    if timestamp is None:
        timestamp = int(time.time())

    url_map = {}
    with open(f"{specification_dir}/collection.csv", newline="") as f:
        for row in csv.DictReader(f):
            collection = row["collection"]
            for file in COLLECTION_FILES:
                output_path = f"var/collection/{collection}/{file}"
                if Path(output_path).exists():  # preserve idempotency skip
                    continue
                url = (
                    f"{S3}{collection}-collection/collection/{file}?version={timestamp}"
                )
                url_map[url] = output_path
    return url_map


@click.command()
@click.option(
    "--specification-dir",
    default="specification",
    help="Directory containing collection.csv",
)
def download_collection(specification_dir):
    download_urls(build_url_map(specification_dir))


if __name__ == "__main__":
    download_collection()
