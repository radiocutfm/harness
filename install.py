# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Bootstrap entry point; reconciliation is tracked in the implementation issues."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path


HARNESS_VERSION = "@HARNESS_VERSION@"
DEFAULT_MODEL = "deepseek/deepseek-v4-flash"


def skill_source(archive: Path | None) -> Path:
    if archive is None:
        return Path(__file__).resolve().parent / "skills"
    directory = Path(tempfile.mkdtemp(prefix="fierro-harness-skills-"))
    with tarfile.open(archive, "r:gz") as bundle:
        root = directory.resolve()
        for member in bundle.getmembers():
            destination = (root / member.name).resolve()
            if root not in destination.parents:
                raise ValueError("El archivo de skills contiene una ruta inválida")
        bundle.extractall(directory)
    return directory / "skills"


def same_tree(left: Path, right: Path) -> bool:
    comparison = filecmp.dircmp(left, right)
    return not comparison.left_only and not comparison.right_only and not comparison.diff_files and all(
        filecmp.cmp(left / name, right / name, shallow=False) for name in comparison.common_files
    ) and all(
        same_tree(left / name, right / name) for name in comparison.common_dirs
    )


def install_skills(source: Path, destination: Path, dry_run: bool) -> int:
    if not source.is_dir():
        raise FileNotFoundError(f"No se encontró el directorio de skills: {source}")
    destination.mkdir(parents=True, exist_ok=True)
    installed = 0
    for skill in sorted(path for path in source.iterdir() if (path / "SKILL.md").is_file()):
        target = destination / skill.name
        if target.exists():
            if not target.is_dir() or not same_tree(skill, target):
                print(f"Conflicto: la skill ya existe y es diferente: {target}", file=sys.stderr)
                return 1
            print(f"Ya instalada: {skill.name}")
            continue
        print(f"Instalar: {skill.name} -> {target}")
        installed += 1
        if not dry_run:
            temporary = Path(tempfile.mkdtemp(prefix=f".{skill.name}-", dir=destination))
            shutil.rmtree(temporary)
            shutil.copytree(skill, temporary)
            temporary.rename(target)
    return 0


def configure_opencode(dry_run: bool) -> int:
    config_dir = Path.home() / ".config" / "opencode"
    config_path = config_dir / "opencode.json"
    state_dir = Path.home() / ".config" / "fierro-harness"
    state_path = state_dir / "opencode-managed.json"
    managed_key = "model"

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
            print(f"No se pudo leer el registro de configuración administrada: {error}", file=sys.stderr)
            return 1

    managed = state.get("managed", {})
    previous = state.get("previous", {})
    owns_model = isinstance(managed, dict) and managed.get(managed_key) == DEFAULT_MODEL
    if managed_key in config and config[managed_key] != DEFAULT_MODEL and not owns_model:
        print(
            f"Conflicto: OpenCode ya define model={config[managed_key]!r}; "
            "no se reemplaza la configuración personal.",
            file=sys.stderr,
        )
        return 1

    if config.get(managed_key) == DEFAULT_MODEL and owns_model:
        print("Configuración de OpenCode ya aplicada")
        return 0

    print(f"Configurar OpenCode: model={DEFAULT_MODEL}")
    if dry_run:
        return 0

    config_dir.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        backup = config_path.with_name(
            f"opencode.json.backup-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
        )
        shutil.copy2(config_path, backup)
    if managed_key not in previous:
        previous[managed_key] = config.get(managed_key)
    config.setdefault("$schema", "https://opencode.ai/config.json")
    config[managed_key] = DEFAULT_MODEL
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps({"managed": {managed_key: DEFAULT_MODEL}, "previous": previous}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install or repair Fierro Agents Harness"
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skills-archive", type=Path)
    args = parser.parse_args()
    mode = "dry-run" if args.dry_run else "plan"
    print(f"Fierro-harness {HARNESS_VERSION}: {mode}")
    source = skill_source(args.skills_archive)
    destination = Path.home() / ".agents" / "skills"
    if install_skills(source, destination, args.dry_run):
        raise SystemExit(1)
    if configure_opencode(args.dry_run):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
