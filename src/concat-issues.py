#!/usr/bin/env python3

import csv
import glob
import re
import os
import click

csv.field_size_limit(10 * 1024 * 1024)

# Otherwise title-boundary creates 54 Million OSGB issues slowing down the issues table
EXCLUDED_DATASETS = {"title-boundary"}


@click.command()
@click.option(
    "--issues-dir", default="issues/", help="Directory where issue.csv will be stored"
)
@click.option(
    "--input-dir", default="var/issue/", help="Directory containing issue CSV files"
)
def process_issues(issues_dir, input_dir):
    """Processes issue CSV files and writes output."""

    fields = [
        "resource",
        "pipeline",
        "row-number",
        "field",
        "issue-type",
        "value",
        "message",
        "dataset",
        "entry-number",
        "line-number",
        "entity",
    ]
    os.makedirs(issues_dir, exist_ok=True)

    # Write to issue.csv
    with open(os.path.join(issues_dir, "issue.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()

        for path in glob.glob(f"{input_dir}/*/*.csv"):
            m = re.search(r"/([a-zA-Z0-9_-]+)/([a-f0-9]+).csv$", path)

            pipeline = m.group(1)
            resource = m.group(2)

            if pipeline in EXCLUDED_DATASETS:
                continue

            with open(path, newline="") as infile:
                for row in csv.DictReader(infile):
                    row["resource"] = resource
                    row["pipeline"] = pipeline
                    w.writerow(row)


if __name__ == "__main__":
    process_issues()
