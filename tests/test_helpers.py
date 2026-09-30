from unittest.mock import Mock

import galaxy_ie_helpers


def _install_clients(monkeypatch, history):
    galaxy = Mock()
    history_client = Mock()
    history_client.show_history.return_value = history
    dataset_client = Mock()
    collection_client = Mock()

    monkeypatch.setattr(
        galaxy_ie_helpers, "get_galaxy_connection", Mock(return_value=galaxy)
    )
    monkeypatch.setattr(
        galaxy_ie_helpers, "HistoryClient", Mock(return_value=history_client)
    )
    monkeypatch.setattr(
        galaxy_ie_helpers, "DatasetClient", Mock(return_value=dataset_client)
    )
    monkeypatch.setattr(
        galaxy_ie_helpers,
        "DatasetCollectionClient",
        Mock(return_value=collection_client),
    )
    return dataset_client, collection_client


def test_get_downloads_and_reuses_cached_dataset(monkeypatch, tmp_path):
    history = [
        {
            "hid": 1,
            "id": "encoded-id",
            "history_content_type": "dataset",
            "extension": "txt",
        }
    ]
    dataset_client, _ = _install_clients(monkeypatch, history)
    monkeypatch.setattr(galaxy_ie_helpers, "IMPORT_DIR", str(tmp_path))

    def download(_dataset_id, *, file_path, use_default_filename):
        assert use_default_filename is False
        with open(file_path, "w") as handle:
            handle.write("contents")

    dataset_client.download_dataset.side_effect = download

    expected = str(tmp_path / "1")
    assert galaxy_ie_helpers.get("1", history_id="history") == expected
    assert galaxy_ie_helpers.get("1", history_id="history") == expected
    dataset_client.download_dataset.assert_called_once()


def test_get_returns_datatype_for_dataset_name(monkeypatch, tmp_path):
    history = [
        {
            "name": "report",
            "id": "encoded-id",
            "history_content_type": "dataset",
            "extension": "tabular",
        }
    ]
    dataset_client, _ = _install_clients(monkeypatch, history)
    monkeypatch.setattr(galaxy_ie_helpers, "IMPORT_DIR", str(tmp_path))
    dataset_client.download_dataset.side_effect = lambda _id, *, file_path, **_kwargs: (
        open(file_path, "w").close()
    )

    paths, datatype = galaxy_ie_helpers.get(
        "report",
        identifier_type="name",
        history_id="history",
        retrieve_datatype=True,
    )

    assert paths == [str(tmp_path / "report")]
    assert datatype == "tabular"


def test_regex_lookup_uses_explicit_history(monkeypatch):
    finder = Mock(return_value=[])
    monkeypatch.setattr(galaxy_ie_helpers, "find_matching_history_ids", finder)
    _install_clients(monkeypatch, [])

    assert (
        galaxy_ie_helpers.get(
            "report.*", identifier_type="regex", history_id="explicit-history"
        )
        == []
    )
    finder.assert_called_once_with(["report.*"], history_id="explicit-history")


def test_fallback_url_preserves_nested_path(monkeypatch):
    attempted_urls = []

    def test_url(url, *_args, **_kwargs):
        attempted_urls.append(url)
        return None

    monkeypatch.setenv("API_KEY", "key")
    monkeypatch.setenv("GALAXY_URL", "https://example.org/galaxy/sub/")
    monkeypatch.setenv("GALAXY_WEB_PORT", "8080")
    monkeypatch.setattr(galaxy_ie_helpers, "_get_ip", Mock(return_value="172.17.0.1"))
    monkeypatch.setattr(galaxy_ie_helpers, "_test_url", test_url)

    try:
        galaxy_ie_helpers.get_galaxy_connection(history_id="history")
    except Exception as exc:
        assert str(exc).startswith("Could not connect")

    assert attempted_urls == [
        "https://example.org/galaxy/sub/",
        "http://172.17.0.1:8080/galaxy/sub",
    ]
