from __future__ import annotations

import json
from pathlib import Path

from fierro_harness import installer


def test_install_is_idempotent_and_configures_model(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))

    assert installer.install() == 0
    config_path = tmp_path / ".config" / "opencode" / "opencode.json"
    assert json.loads(config_path.read_text()) ["model"] == installer.DEFAULT_MODEL

    assert installer.install() == 0
    assert (tmp_path / ".agents" / "skills" / "scripting-python" / "SKILL.md").exists()


def test_install_preserves_personal_model(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    config_dir = tmp_path / ".config" / "opencode"
    config_dir.mkdir(parents=True)
    config_path = config_dir / "opencode.json"
    config_path.write_text('{"model": "personal/provider"}\n')

    assert installer.install() == 1
    assert json.loads(config_path.read_text())["model"] == "personal/provider"
