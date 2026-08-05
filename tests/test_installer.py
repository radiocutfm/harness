from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from fierro_harness import cli, installer, tools
from fierro_harness.cli import app
from fierro_harness.tools import (
    TOOLS_BY_NAME,
    ToolSpec,
    ToolStatus,
    installation_plan,
    normalize_system,
    version_at_least,
)

runner = CliRunner()


def test_install_is_idempotent_and_configures_model(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))

    assert installer.install() == 0
    config_path = tmp_path / ".config" / "opencode" / "opencode.json"
    assert json.loads(config_path.read_text())["model"] == installer.DEFAULT_MODEL

    assert installer.install() == 0
    assert (tmp_path / ".agents" / "skills" / "scripting-python" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "trello" / "references" / "conectar-trello.md").exists()


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
    assert "throw 'Checksum inválido'" in installation_plan(TOOLS_BY_NAME["jq"], system="Windows")[1]
    assert "trello-cli_0.1.1_linux_amd64" in installation_plan(TOOLS_BY_NAME["trello-cli"], system="Linux")[0]


def test_platform_names_are_normalized_before_plan_lookup() -> None:
    assert normalize_system("Darwin") == "macos"
    assert "install.sh" in TOOLS_BY_NAME["uv"].installation_plan("Darwin").commands[0]
    assert TOOLS_BY_NAME["jq"].supports("Darwin")
    assert "jq-macos" in installation_plan(TOOLS_BY_NAME["jq"], system="Darwin")[0]


def test_typer_cli_renders_a_tool_plan() -> None:
    result = runner.invoke(app, ["tools", "--plan", "jq"])
    assert result.exit_code == 0
    assert "jq-1.8.2" in result.output


def test_typer_cli_rejects_unknown_tool_plan() -> None:
    result = runner.invoke(app, ["tools", "--plan", "unknown"])
    assert result.exit_code == 2
    assert "herramienta desconocida" in result.output


def test_plans_are_explicit_for_each_core_tool() -> None:
    assert "astral.sh" in installation_plan(TOOLS_BY_NAME["uv"], system="Linux")[0]
    assert "opencode-ai@1.18.13" in installation_plan(TOOLS_BY_NAME["opencode"], system="Linux")[0]


def test_opencode_desktop_plans_use_official_pinned_artifacts_and_checksums() -> None:
    linux_plan = installation_plan(TOOLS_BY_NAME["opencode-desktop"], system="Linux")[0]
    windows_plan = installation_plan(TOOLS_BY_NAME["opencode-desktop"], system="Windows")[0]

    assert "opencode-desktop-linux-amd64.deb" in linux_plan
    assert "opencode-desktop-linux-x86_64.rpm" in linux_plan
    assert "sha256sum -c" in linux_plan
    assert "sudo dpkg -i" in linux_plan
    assert "opencode-desktop-win-x64.exe" in windows_plan
    assert "Get-FileHash" in windows_plan


def test_opencode_desktop_is_detected_without_a_path_command(tmp_path: Path, monkeypatch) -> None:
    application = tmp_path / "Programs" / "OpenCode" / "OpenCode.exe"
    application.parent.mkdir(parents=True)
    application.touch()
    monkeypatch.setattr(tools.platform, "system", lambda: "Windows")
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))

    status = tools.inspect_tool(TOOLS_BY_NAME["opencode-desktop"])

    assert status.installed
    assert status.version is None
    assert status.error is None


def test_setup_allows_environment_confirmation(monkeypatch) -> None:
    installed: list[str] = []
    monkeypatch.setenv("FIERRO_HARNESS_ASSUME_YES", "1")
    monkeypatch.setattr("fierro_harness.cli.install_tool", lambda tool, dry_run: installed.append(tool.name))

    result = runner.invoke(app, ["setup", "--install", "opencode-desktop"])

    assert result.exit_code == 0
    assert installed == ["opencode-desktop"]


def test_version_flag_and_install_command(monkeypatch) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip()

    monkeypatch.setattr(cli, "reconcile_install", lambda dry_run: 0)
    result = runner.invoke(app, ["install", "--dry-run"])
    assert result.exit_code == 0
    assert "simulación" in result.output


def test_tools_reports_json_and_text_states(monkeypatch) -> None:
    statuses = [
        ToolStatus("ok", "1", True, "ok 1", True, "source"),
        ToolStatus("old", "2", False, "old 1", True, "source", "version is too old"),
        ToolStatus("missing", "3", False, None, True, "source", "not found"),
    ]
    monkeypatch.setattr(cli, "inspect_tools", lambda: statuses)

    result = runner.invoke(app, ["tools", "--json"])
    assert result.exit_code == 1
    assert '"name": "ok"' in result.output

    result = runner.invoke(app, ["tools"])
    assert result.exit_code == 1
    assert "desactualizada" in result.output
    assert "ausente" in result.output


def test_tools_rejects_unsupported_plan(monkeypatch) -> None:
    monkeypatch.setattr(cli, "installation_plan", lambda tool: (_ for _ in ()).throw(ValueError("plataforma inválida")))

    result = runner.invoke(app, ["tools", "--plan", "uv"])

    assert result.exit_code == 2
    assert "plataforma inválida" in result.output


def test_setup_reports_statuses_and_rejects_unknown(monkeypatch) -> None:
    statuses = [ToolStatus("uv", "1", False, None, True, "source")]
    monkeypatch.setattr(cli, "inspect_tools", lambda: statuses)

    unknown = runner.invoke(app, ["setup", "--install", "unknown"])
    assert unknown.exit_code == 2
    assert "herramienta desconocida" in unknown.output

    text = runner.invoke(app, ["setup"])
    assert text.exit_code == 1
    assert "pendiente" in text.output

    as_json = runner.invoke(app, ["setup", "--json"])
    assert as_json.exit_code == 1
    assert '"name": "uv"' in as_json.output


def test_setup_prints_plan_before_confirmation(monkeypatch) -> None:
    monkeypatch.setattr(cli, "inspect_tools", lambda: [])
    monkeypatch.setattr(cli, "installation_plan", lambda tool: ("comando de prueba",))

    result = runner.invoke(app, ["setup", "--install", "uv"])

    assert result.exit_code == 1
    assert "comando de prueba" in result.output
    assert "FIERRO_HARNESS_ASSUME_YES" in result.output


def test_main_delegates_to_typer(monkeypatch) -> None:
    called = []
    monkeypatch.setattr(cli, "app", lambda: called.append(True))

    cli.main()

    assert called == [True]


def test_same_tree_and_install_skills_error_paths(tmp_path: Path) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    skill = source / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("skill")
    destination.mkdir()
    conflict = destination / skill.name
    conflict.mkdir()
    (conflict / "SKILL.md").write_text("other")
    assert not installer.same_tree(source, destination)
    assert installer.same_tree(source, source)

    with pytest.raises(FileNotFoundError):
        installer.install_skills(tmp_path / "missing", destination, dry_run=False)
    assert installer.install_skills(source, tmp_path / "dry", dry_run=True) == 0
    assert installer.install_skills(source, destination, dry_run=False) == 1


def test_configure_opencode_handles_invalid_files_conflicts_and_dry_run(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    config_path = tmp_path / ".config" / "opencode" / "opencode.json"
    config_path.parent.mkdir(parents=True)

    config_path.write_text("invalid")
    assert installer.configure_opencode(dry_run=False) == 1
    config_path.write_text("[]")
    assert installer.configure_opencode(dry_run=False) == 1
    config_path.write_text('{"model": "personal/provider"}')
    assert installer.configure_opencode(dry_run=False) == 1
    config_path.write_text("{}")
    assert installer.configure_opencode(dry_run=True) == 0

    state_path = tmp_path / ".config" / "fierro-harness" / "opencode-managed.json"
    state_path.parent.mkdir(parents=True)
    state_path.write_text("invalid")
    assert installer.configure_opencode(dry_run=False) == 1
    config_path.write_text("{}")
    state_path.write_text("{}")
    assert installer.configure_opencode(dry_run=False) == 0
    state_path.write_text(json.dumps({"managed": {"model": installer.DEFAULT_MODEL}}))
    config_path.write_text(json.dumps({"model": installer.DEFAULT_MODEL}))
    assert installer.configure_opencode(dry_run=False) == 0


def test_install_returns_failure_when_skills_cannot_install(monkeypatch) -> None:
    monkeypatch.setattr(installer, "install_skills", lambda source, destination, dry_run: 1)

    assert installer.install() == 1


def test_tool_spec_and_inspection_error_paths(tmp_path: Path, monkeypatch) -> None:
    spec = TOOLS_BY_NAME["uv"]
    assert spec.supports("FreeBSD") is False
    with pytest.raises(ValueError, match="Unsupported platform"):
        spec.installation_plan("FreeBSD")
    linux_only = ToolSpec("linux", "linux", "1", "source", {"linux": tools.InstallPlan(("echo",))})
    with pytest.raises(ValueError, match="not supported"):
        linux_only.installation_plan("Darwin")
    with pytest.raises(ValueError, match="no tiene un comando"):
        tools._version_command(TOOLS_BY_NAME["opencode-desktop"])
    with pytest.raises(ValueError, match="Unsupported platform"):
        normalize_system("FreeBSD")
    assert not version_at_least("sin versión", "1.0")

    monkeypatch.setattr(tools.platform, "system", lambda: "FreeBSD")
    assert tools._detection_path(TOOLS_BY_NAME["opencode-desktop"]) is None
    monkeypatch.setattr(tools.platform, "system", lambda: "Linux")
    assert not tools.inspect_tool(TOOLS_BY_NAME["opencode-desktop"]).installed

    monkeypatch.setattr(tools.shutil, "which", lambda command: None)
    assert not tools.inspect_tool(spec).installed

    monkeypatch.setattr(tools.shutil, "which", lambda command: "/usr/bin/uv")

    def raising_run(*args, **kwargs):
        raise OSError("falló")

    assert "falló" in (tools.inspect_tool(spec, run=raising_run).error or "")

    def failed_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, "", "falló")

    failed = tools.inspect_tool(spec, run=failed_run)
    assert failed.error == "falló"

    def empty_failed_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 1, "", "")

    assert tools.inspect_tool(spec, run=empty_failed_run).error == "version command failed"

    def old_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, "uv 0.1.0", "")

    assert tools.inspect_tool(spec, run=old_run).error == "version is too old"


def test_tool_helpers_serialize_and_install(monkeypatch) -> None:
    statuses = [ToolStatus("tool", "1", True, "1", True, "source")]
    monkeypatch.setattr(tools, "inspect_tools", lambda: statuses)
    assert '"tool"' in tools.tool_status_json()

    spec = ToolSpec("tool", "tool", "1", "source", {"linux": tools.InstallPlan(("echo ok",))})
    executed = []
    monkeypatch.setattr(tools.subprocess, "run", lambda command, **kwargs: executed.append((command, kwargs)))
    tools.install_tool(spec, dry_run=False, system="Linux")
    tools.install_tool(spec, dry_run=True, system="Linux")
    assert executed == [("echo ok", {"shell": True, "check": True})]
