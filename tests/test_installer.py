from __future__ import annotations

import json
from pathlib import Path

from fierro_harness import installer
from fierro_harness.tools import TOOLS_BY_NAME, installation_plan, normalize_system, version_at_least


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


def test_version_at_least_handles_prefixes_and_suffixes() -> None:
    assert version_at_least("uv 0.12.1", "0.11.0")
    assert version_at_least("jq-1.8.2", "1.8.2")
    assert not version_at_least("opencode 1.18.12", "1.18.13")


def test_jq_plan_uses_a_pinned_release_and_checksum() -> None:
    plan = installation_plan(TOOLS_BY_NAME["jq"], system="Linux")
    assert "jq-1.8.2" in plan[0]
    assert "sha256sum -c" in plan[1]


def test_platform_names_are_normalized_before_plan_lookup() -> None:
    assert normalize_system("Darwin") == "macos"
    assert "install.sh" in TOOLS_BY_NAME["uv"].installation_plan("Darwin").commands[0]
