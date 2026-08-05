"""Install skills and the managed OpenCode defaults."""

from __future__ import annotations

import filecmp
import json
import shutil
import sys
import tempfile
from datetime import UTC, datetime
from importlib.resources import as_file, files
from pathlib import Path
from typing import cast

DEFAULT_MODEL = "deepseek/deepseek-v4-flash"


def same_tree(left: Path, right: Path) -> bool:
    """Return whether two directory trees have the same files and content."""
    comparison = filecmp.dircmp(left, right)
    return (
        not comparison.left_only
        and not comparison.right_only
        and not comparison.diff_files
        and all(filecmp.cmp(left / name, right / name, shallow=False) for name in comparison.common_files)
        and all(same_tree(left / name, right / name) for name in comparison.common_dirs)
    )


def install_skills(source: Path, destination: Path, dry_run: bool) -> int:
    """Install bundled skills without overwriting a different personal skill."""
    if not source.is_dir():
        raise FileNotFoundError(f"No se encontró el directorio de skills: {source}")
    if not dry_run:
        destination.mkdir(parents=True, exist_ok=True)
    for skill in sorted(path for path in source.iterdir() if (path / "SKILL.md").is_file()):
        target = destination / skill.name
        if target.exists():
            if not target.is_dir() or not same_tree(skill, target):
                print(f"Conflicto: la skill ya existe y es diferente: {target}", file=sys.stderr)
                return 1
            print(f"Ya instalada: {skill.name}")
            continue
        print(f"Instalar: {skill.name} -> {target}")
        if not dry_run:
            temporary = Path(tempfile.mkdtemp(prefix=f".{skill.name}-", dir=destination))
            shutil.rmtree(temporary)
            shutil.copytree(skill, temporary)
            temporary.rename(target)
    return 0


def configure_opencode(dry_run: bool) -> int:
    """Merge the managed model default while preserving personal settings."""
    config_dir = Path.home() / ".config" / "opencode"
    config_path = config_dir / "opencode.json"
    state_dir = Path.home() / ".config" / "fierro-harness"
    state_path = state_dir / "opencode-managed.json"
    config: dict[str, object] = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            print(f"No se pudo leer la configuración de OpenCode: {error}", file=sys.stderr)
            return 1
        if not isinstance(config, dict):
            print("La configuración de OpenCode debe ser un objeto JSON", file=sys.stderr)
            return 1

    state: dict[str, object] = {}
    if state_path.exists():
        try:
            loaded = json.loads(state_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                state = loaded
        except (OSError, json.JSONDecodeError) as error:
            print(f"No se pudo leer el registro administrado: {error}", file=sys.stderr)
            return 1

    managed_value = state.get("managed", {})
    managed = managed_value if isinstance(managed_value, dict) else {}
    previous_value = state.get("previous", {})
    previous = cast("dict[str, object]", previous_value) if isinstance(previous_value, dict) else {}
    owns_model = isinstance(managed, dict) and managed.get("model") == DEFAULT_MODEL
    if "model" in config and config["model"] != DEFAULT_MODEL and not owns_model:
        print(f"Conflicto: OpenCode ya define model={config['model']!r}; no se reemplaza.", file=sys.stderr)
        return 1
    if config.get("model") == DEFAULT_MODEL and owns_model:
        print("Configuración de OpenCode ya aplicada")
        return 0

    print(f"Configurar OpenCode: model={DEFAULT_MODEL}")
    if dry_run:
        return 0
    config_dir.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        backup = config_path.with_name(f"opencode.json.backup-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}")
        shutil.copy2(config_path, backup)
    if "model" not in previous:
        previous["model"] = config.get("model")
    config.setdefault("$schema", "https://opencode.ai/config.json")
    config["model"] = DEFAULT_MODEL
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps({"managed": {"model": DEFAULT_MODEL}, "previous": previous}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


def install(*, dry_run: bool = False) -> int:
    """Install bundled resources and managed configuration."""
    source = files("fierro_harness").joinpath("resources", "skills")
    with as_file(source) as source_path:
        destination = Path.home() / ".agents" / "skills"
        if install_skills(source_path, destination, dry_run):
            return 1
    return configure_opencode(dry_run)
