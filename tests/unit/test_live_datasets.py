import pytest

from live_datasets import live_datasets

SPEC_CSV = """dataset,end-date
in-production,
in-staging,
in-development,
switched-off,
end-dated,2026-02-03
"""

CONFIG_CSV = """dataset,environment
in-production,production
in-staging,staging
in-development,development
switched-off,
end-dated,production
"""


@pytest.fixture
def specification_dir(tmp_path):
    (tmp_path / "dataset.csv").write_text(SPEC_CSV)
    return str(tmp_path)


@pytest.fixture
def config_path(tmp_path):
    path = tmp_path / "config.csv"
    path.write_text(CONFIG_CSV)
    return str(path)


@pytest.mark.parametrize(
    "env, expected",
    [
        ("production", {"in-production"}),
        ("staging", {"in-production", "in-staging"}),
        ("development", {"in-production", "in-staging", "in-development"}),
    ],
)
def test_live_datasets_for_each_environment(
    specification_dir, config_path, env, expected
):
    assert live_datasets(specification_dir, env, config_path) == expected


def test_no_environment_means_no_filter(specification_dir, config_path):
    assert live_datasets(specification_dir, None, config_path) is None


def test_no_live_datasets_means_no_filter(tmp_path):
    (tmp_path / "dataset.csv").write_text("dataset,end-date\n")
    (tmp_path / "config.csv").write_text("dataset,environment\n")
    assert (
        live_datasets(str(tmp_path), "production", str(tmp_path / "config.csv")) is None
    )


def test_dataset_missing_from_config_is_not_live(tmp_path):
    (tmp_path / "dataset.csv").write_text(
        "dataset,end-date\nnew-one,\nin-production,\n"
    )
    (tmp_path / "config.csv").write_text(
        "dataset,environment\nin-production,production\n"
    )
    assert live_datasets(str(tmp_path), "production", str(tmp_path / "config.csv")) == {
        "in-production"
    }
