# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Bootstrap entry point; reconciliation is tracked in the implementation issues."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path


HARNESS_VERSION = "@HARNESS_VERSION@"


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


if __name__ == "__main__":
    main()
