#!/usr/bin/env python3
import csv
import logging
import time
from pathlib import Path

import click

from file_downloader import download_urls

logger = logging.getLogger(__name__)

S3 = "https://files.planning.data.gov.uk/"
OPERATIONAL_ISSUE_DIR = "performance/operational_issue/"


def build_url_map(specification_dir="specification", timestamp=None):
    """Build {url: output_path} for every dataset's operational-issue file."""
    if timestamp is None:
        timestamp = int(time.time())

    url_map = {}
    with open(f"{specification_dir}/dataset.csv", newline="") as f:
        for row in csv.DictReader(f):
            dataset = row["dataset"]
            if not dataset:
                continue
            output_path = f"{OPERATIONAL_ISSUE_DIR}{dataset}/operational-issue.csv"
            if Path(output_path).exists():  # preserve idempotency skip
                continue
            url = f"{S3}{OPERATIONAL_ISSUE_DIR}{dataset}/operational-issue.csv?version={timestamp}"
            url_map[url] = output_path
    return url_map


@click.command()
@click.option(
    "--specification-dir",
    default="specification",
    help="Directory containing dataset.csv",
)
def download_operational_issues(specification_dir):
    download_urls(build_url_map(specification_dir))


if __name__ == "__main__":
    download_operational_issues()
