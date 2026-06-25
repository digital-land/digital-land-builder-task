#!/usr/bin/env python3
import csv
import logging
from pathlib import Path

import click

from file_downloader import download_urls

logger = logging.getLogger(__name__)

GITHUB = "https://raw.githubusercontent.com/digital-land/"
PIPELINE_FILES = [
    "column.csv",
    "combine.csv",
    "concat.csv",
    "convert.csv",
    "default.csv",
    "default-value.csv",
    "patch.csv",
    "plugins.py",
    "skip.csv",
    "transform.csv",
    "filter.csv",
    "lookup.csv",
]


def build_url_map(specification_dir="specification"):
    """Build {url: output_path} for every collection's pipeline config files."""
    url_map = {}
    with open(f"{specification_dir}/collection.csv", newline="") as f:
        for row in csv.DictReader(f):
            collection = row["collection"]
            for file in PIPELINE_FILES:
                output_path = f"var/pipeline/{collection}/{file}"
                if Path(output_path).exists():  # preserve idempotency skip
                    continue
                url = f"{GITHUB}config/main/pipeline/{collection}/{file}"
                url_map[url] = output_path
    return url_map


@click.command()
@click.option(
    "--specification-dir",
    default="specification",
    help="Directory containing collection.csv",
)
def download_pipeline(specification_dir):
    download_urls(build_url_map(specification_dir))


if __name__ == "__main__":
    download_pipeline()
