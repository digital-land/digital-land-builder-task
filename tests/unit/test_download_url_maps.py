import download_collection
import download_pipeline


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
