import csv
import importlib.util
from pathlib import Path

from click.testing import CliRunner

# concat-issues.py is hyphenated so it cannot be imported normally
MODULE_PATH = Path(__file__).parents[2] / "src" / "concat-issues.py"

FIELDS = [
    "field",
    "issue-type",
    "value",
    "line-number",
    "entry-number",
    "entity",
    "dataset",
    "message",
]


def _load():
    spec = importlib.util.spec_from_file_location("concat_issues", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_issue_csv(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerow(
            {
                "field": "geometry",
                "issue-type": "OSGB",
                "value": "",
                "line-number": 1,
                "entry-number": 1,
                "entity": 1,
                "dataset": "x",
                "message": "",
            }
        )


def test_excluded_dataset_issues_are_not_written(tmp_path):
    module = _load()
    input_dir = tmp_path / "issue"
    resource = "a" * 8
    _write_issue_csv(input_dir / "title-boundary" / f"{resource}.csv")
    _write_issue_csv(input_dir / "conservation-area" / f"{resource}.csv")

    out = tmp_path / "issues"
    result = CliRunner().invoke(
        module.process_issues,
        [
            "--issues-dir",
            str(out),
            "--operational-issue-dir",
            str(tmp_path / "op"),
            "--input-dir",
            str(input_dir),
        ],
    )
    assert result.exit_code == 0, result.output

    rows = list(csv.DictReader(open(out / "issue.csv")))
    assert {row["pipeline"] for row in rows} == {"conservation-area"}
