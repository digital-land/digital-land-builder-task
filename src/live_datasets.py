#!/usr/bin/env python3
import csv
import logging

logger = logging.getLogger(__name__)


def live_datasets(specification_dir, env):
    """The datasets the platform builds in `env` and has not retired.

    Mirrors is_dataset_available in airflow-dags (dags/utils.py) and
    live_datasets in pyspark-jobs (src/jobs/pipeline/authority.py): a
    `production` dataset is built in every environment, `staging` only in
    staging and development, `development` only in development, and a blank
    environment is not built anywhere. An end-dated dataset is retired
    whatever its environment.

    Returns None, meaning don't filter, when env isn't set (a local run) or
    when no dataset is live, which means the specification is broken rather
    than that every dataset has been switched off.
    """
    if not env:
        logger.warning("ENVIRONMENT not set, so not filtering by live datasets")
        return None

    available = {"production"}
    if env in ("staging", "development"):
        available.add("staging")
    if env == "development":
        available.add("development")

    with open(f"{specification_dir}/dataset.csv", newline="") as f:
        datasets = {
            row["dataset"]
            for row in csv.DictReader(f)
            if row["environment"] in available and not row["end-date"]
        }

    if not datasets:
        logger.error(
            f"no live datasets found in {specification_dir}/dataset.csv for {env}, so not filtering"
        )
        return None

    return datasets
