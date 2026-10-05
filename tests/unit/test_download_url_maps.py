import download_collection
import download_column_field
import download_converted_resources
import download_issues
import download_pipeline

PA_BASE = "https://files.planning.data.gov.uk/planning-application-collection"
ISSUE_BASE = f"{PA_BASE}/issue"
ISSUE_RESOURCES = {
    "aaa": {
        "collection": "planning-application",
        "pipelines": {"planning-application": True, "planning-application-type": True},
    }
}


def test_collection_url_map(tmp_path):
    spec = tmp_path / "specification"
    spec.mkdir()
    (spec / "collection.csv").write_text("collection\nancient-woodland\n")

    url_map = download_collection.build_url_map(str(spec), timestamp=123)

    base = "https://files.planning.data.gov.uk/ancient-woodland-collection/collection"
    assert url_map == {
        f"{base}/endpoint.csv?version=123": "var/collection/ancient-woodland/endpoint.csv",
        f"{base}/source.csv?version=123": "var/collection/ancient-woodland/source.csv",
        f"{base}/log.csv?version=123": "var/collection/ancient-woodland/log.csv",
        f"{base}/resource.csv?version=123": "var/collection/ancient-woodland/resource.csv",
        f"{base}/old-resource.csv?version=123": "var/collection/ancient-woodland/old-resource.csv",
    }


def test_pipeline_url_map(tmp_path):
    spec = tmp_path / "specification"
    spec.mkdir()
    (spec / "collection.csv").write_text("collection\nancient-woodland\n")

    url_map = download_pipeline.build_url_map(str(spec))

    base = "https://raw.githubusercontent.com/digital-land/config/main/pipeline/ancient-woodland"
    # every pipeline file should map to its var/pipeline path
    assert len(url_map) == len(download_pipeline.PIPELINE_FILES)
    assert url_map[f"{base}/column.csv"] == "var/pipeline/ancient-woodland/column.csv"
    assert url_map[f"{base}/plugins.py"] == "var/pipeline/ancient-woodland/plugins.py"


def test_issue_url_map_without_filter():
    url_map = download_issues.build_url_map(ISSUE_RESOURCES, timestamp=123)

    assert url_map == {
        f"{ISSUE_BASE}/planning-application/aaa.csv?version=123": "var/issue/planning-application/aaa.csv",
        f"{ISSUE_BASE}/planning-application-type/aaa.csv?version=123": "var/issue/planning-application-type/aaa.csv",
    }


def test_issue_url_map_skips_datasets_that_are_not_live():
    url_map = download_issues.build_url_map(
        ISSUE_RESOURCES, datasets={"planning-application-type"}, timestamp=123
    )

    assert url_map == {
        f"{ISSUE_BASE}/planning-application-type/aaa.csv?version=123": "var/issue/planning-application-type/aaa.csv",
    }


def test_column_field_url_map_skips_datasets_that_are_not_live():
    url_map = download_column_field.build_url_map(
        ISSUE_RESOURCES, datasets={"planning-application-type"}, timestamp=123
    )

    assert url_map == {
        f"{PA_BASE}/var/column-field/planning-application-type/aaa.csv?version=123": "var/column-field/planning-application-type/aaa.csv",
    }


def test_converted_resource_url_map_skips_datasets_that_are_not_live():
    url_map = download_converted_resources.build_url_map(
        ISSUE_RESOURCES, datasets={"planning-application-type"}, timestamp=123
    )

    assert url_map == {
        f"{PA_BASE}/var/converted-resource/planning-application-type/aaa.csv?version=123": "var/converted-resource/planning-application-type/aaa.csv",
    }
