from importlib.metadata import metadata


def test_project_version():
    project = metadata("galaxy-ie-helpers")

    assert project["Version"] == "0.3.0"
    assert project["Requires-Python"] == ">=3.10"
