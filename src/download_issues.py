#!/usr/bin/env python3
import logging
import os
import click
from datetime import datetime

from resources import get_resources
from file_downloader import download_urls
from live_datasets import live_datasets


logger = logging.getLogger("__name__")


def build_url_map(resources, datasets=None, timestamp=None):
    """Build {url: output_path} for every resource's issue files.

    When datasets is given, pipelines not in it are skipped: a dataset switched
    off for this environment keeps its frozen issue files in the bucket, and
    they would otherwise be loaded into digital-land every night.
    """
    url_map = {}
    skipped = set()

    for resource in resources:
        collection = resources[resource]["collection"]
        for pipeline in resources[resource]["pipelines"]:
            if not pipeline:
                logger.error(
                    f"no pipeline for {resource} in {collection} so cannot download"
                )
            elif datasets is not None and pipeline not in datasets:
                skipped.add(pipeline)
            else:
                url = f"https://files.planning.data.gov.uk/{collection}-collection/issue/{pipeline}/{resource}.csv?version={timestamp}"
                output_path = f"var/issue/{pipeline}/{resource}.csv"
                url_map[url] = output_path

    if skipped:
        logger.info(f"skipping issues for datasets that aren't live: {sorted(skipped)}")
    return url_map


@click.command()
@click.option(
    "--specification-dir",
    default="specification",
    help="Directory containing dataset.csv",
)
def download_issues(specification_dir):
    now = datetime.now()
    timestamp = int(now.replace(minute=0, second=0, microsecond=0).timestamp())
    datasets = live_datasets(specification_dir, os.environ.get("ENVIRONMENT"))
    download_urls(build_url_map(get_resources("collection/"), datasets, timestamp))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    download_issues()
