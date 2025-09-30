import pytest
from src.csvcat import as_date, as_timestamp


def test_as_timestamp_valid_formats():
    assert as_timestamp("2025-09-01") == "2025-09-01T00:00:00Z"
    assert as_timestamp("2025-09") == "2025-09-01T00:00:00Z"
    assert as_timestamp("2025") == "2025-01-01T00:00:00Z"
    assert as_timestamp("2025-09-01T00:00:00Z") == "2025-09-01T00:00:00Z"
    assert as_timestamp("2025-09-01T00:00:00+0000") == "2025-09-01T00:00:00Z"


def test_as_timestamp_raise_error():
    with pytest.raises(ValueError):
        as_timestamp("2025-09-01T00:00")
    with pytest.raises(ValueError):
        as_timestamp("01-09-2025")
    with pytest.raises(ValueError):
        as_timestamp("2025/09/01")


def test_as_date_valid_formats():
    assert as_date("2025-09-01") == "2025-09-01"
    assert as_date("2025-09") == "2025-09-01"
    assert as_date("2025") == "2025-01-01"


def test_as_date_raise_error():
    with pytest.raises(ValueError):
        as_date("2025-09/01")
    with pytest.raises(ValueError):
        as_date("01/2025")
    with pytest.raises(ValueError):
        as_date("202509/01")
