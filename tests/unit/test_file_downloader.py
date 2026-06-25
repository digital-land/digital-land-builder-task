import io
import urllib.error
from unittest import mock

import file_downloader


def _http_error(code):
    return urllib.error.HTTPError(
        url="http://x", code=code, msg="err", hdrs=None, fp=None
    )


def test_success_writes_file(tmp_path):
    out = tmp_path / "sub" / "file.csv"
    fake_response = io.BytesIO(b"hello,world\n")

    with mock.patch("file_downloader.urllib.request.urlopen") as urlopen:
        urlopen.return_value.__enter__.return_value = fake_response
        result = file_downloader.download_file("http://x/file.csv", out)

    assert result == out
    assert out.read_bytes() == b"hello,world\n"


def test_404_skips_without_retry(tmp_path):
    out = tmp_path / "missing.csv"

    with mock.patch("file_downloader.urllib.request.urlopen") as urlopen:
        urlopen.side_effect = _http_error(404)
        result = file_downloader.download_file("http://x/missing.csv", out)

    assert result is None  # skipped
    assert urlopen.call_count == 1  # not retried
    assert not out.exists()  # no file written


def test_5xx_retries_then_gives_up(tmp_path):
    out = tmp_path / "flaky.csv"

    with mock.patch("file_downloader.time.sleep"), mock.patch(
        "file_downloader.urllib.request.urlopen"
    ) as urlopen:
        urlopen.side_effect = _http_error(503)
        result = file_downloader.download_file("http://x/flaky.csv", out, max_retries=3)

    assert result is None
    assert urlopen.call_count == 3  # retried up to max_retries
    assert not out.exists()


def test_recovers_after_transient_error(tmp_path):
    out = tmp_path / "ok.csv"
    fake_response = io.BytesIO(b"data")

    ok = mock.MagicMock()
    ok.__enter__.return_value = fake_response

    with mock.patch("file_downloader.time.sleep"), mock.patch(
        "file_downloader.urllib.request.urlopen"
    ) as urlopen:
        urlopen.side_effect = [_http_error(500), ok]  # fail once, then succeed
        result = file_downloader.download_file("http://x/ok.csv", out, max_retries=3)

    assert result == out
    assert urlopen.call_count == 2
    assert out.read_bytes() == b"data"
