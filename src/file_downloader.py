"""
Module containing code to commplete multithreaded downloads using python.
"""

import logging
import sys
from tqdm import tqdm

from pathlib import Path
from urllib.request import urlretrieve
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("__name__")


def download_file(url, output_path, raise_error=False, max_retries=5):
    """Downloads a file using urllib and saves it to the output directory."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    retries = 0
    while retries < max_retries:
        try:
            urlretrieve(url, output_path)
            break
        except Exception as e:
            if raise_error:
                raise e
            else:
                logger.error(f"error downloading file from url {url}: {e}")
        retries += 1


def download_urls(url_map, max_threads=4):
    """Downloads multiple files concurrently using threads."""

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {
            executor.submit(download_file, url, output_path): url
            for url, output_path in url_map.items()
        }
        results = []
        total = len(futures)
        interactive = sys.stdout.isatty()
        last_logged_pct = -1
        for i, future in enumerate(
            tqdm(futures, desc="Downloading files", disable=not interactive), start=1
        ):
            try:
                results.append(future.result())
            except Exception as e:
                logger.errors(f"Error during download: {e}")
            if not interactive:
                pct = (i * 100) // total
                milestone = (pct // 10) * 10
                if milestone > last_logged_pct:
                    logger.info(f"Download progress: {milestone}% ({i}/{total})")
                    last_logged_pct = milestone
        return results
