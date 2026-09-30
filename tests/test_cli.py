import json
import sys
from unittest.mock import Mock

from galaxy_ie_helpers import cli


def test_get_user_history_prints_json(monkeypatch, capsys):
    history = [{"id": "dataset-id", "name": "example"}]
    get_user_history = Mock(return_value=history)
    monkeypatch.setattr(cli.galaxy_ie_helpers, "get_user_history", get_user_history)
    monkeypatch.setattr(sys, "argv", ["get_user_history", "--history-id", "history"])

    cli.get_user_history()

    assert json.loads(capsys.readouterr().out) == history
    get_user_history.assert_called_once_with(history_id="history")
