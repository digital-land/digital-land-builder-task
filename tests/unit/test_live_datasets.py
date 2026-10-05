import pytest

from live_datasets import live_datasets

DATASET_CSV = """dataset,environment,end-date
in-production,production,
in-staging,staging,
in-development,development,
switched-off,,
end-dated,production,2026-02-03
"""


@pytest.fixture
def specification_dir(tmp_path):
    (tmp_path / "dataset.csv").write_text(DATASET_CSV)
    return str(tmp_path)


@pytest.mark.parametrize(
    "env, expected",
    [
        ("production", {"in-production"}),
        ("staging", {"in-production", "in-staging"}),
        ("development", {"in-production", "in-staging", "in-development"}),
    ],
)
def test_live_datasets_for_each_environment(specification_dir, env, expected):
    assert live_datasets(specification_dir, env) == expected


def test_no_environment_means_no_filter(specification_dir):
    assert live_datasets(specification_dir, None) is None


def test_no_live_datasets_means_no_filter(tmp_path):
    """An empty or broken specification must not hide every dataset's issues"""
    (tmp_path / "dataset.csv").write_text("dataset,environment,end-date\n")
    assert live_datasets(str(tmp_path), "production") is None
