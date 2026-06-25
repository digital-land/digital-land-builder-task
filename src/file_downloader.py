"""
Module containing code to complete multithreaded downloads using python.
"""

import logging
import shutil
import socket
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

logger = logging.getLogger(__name__)


def download_file(url, output_path, timeout=60, max_retries=5):
    """Download a single file to output_path.

    Returns the output path on success, or None if the file is absent
    (HTTP 4xx) or could not be fetched after retries. Only transient
    failures (5xx, network errors, timeouts) are retried.
    """
    output_path = Path(output_path)
    last_error = None

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    shutil.copyfileobj(response, f)
            return output_path
        except urllib.error.HTTPError as e:
            # 4xx = file genuinely not there / not accessible; don't retry.
            if 400 <= e.code < 500:
                logger.debug("skipping %s (HTTP %s)", url, e.code)
                return None
            last_error = e
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            last_error = e

        # transient failure: back off and retry
        if attempt < max_retries - 1:
            time.sleep(min(2**attempt, 10))

    logger.error(
        "failed to download %s after %s attempts: %s", url, max_retries, last_error
    )
    return None


def download_urls(url_map, max_threads=16, timeout=30):
    """Download multiple files concurrently. url_map is {url: output_path}."""
    results = []
    failures = 0

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {
            executor.submit(download_file, url, path, timeout): url
            for url, path in url_map.items()
        }
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Downloading files"
        ):
            url = futures[future]
            try:
                result = future.result()
                if result is None:
                    failures += 1
                else:
                    results.append(result)
            except Exception as e:
                failures += 1
                logger.error("error during download of %s: %s", url, e)

    logger.info("downloaded %s files, %s missing/failed", len(results), failures)
    return results
