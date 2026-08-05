"""Detection and opt-in installation plans for harness command-line tools."""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


@dataclass(frozen=True)
class InstallPlan:
    """Reviewed commands for installing one tool on one platform."""

    commands: tuple[str, ...]


@dataclass(frozen=True)
class ToolSpec:
    """The stable contract for a command or desktop application used by skills."""

    name: str
    command: str | None
    minimum_version: str
    source: str
    install_plans: Mapping[str, InstallPlan]
    detection_paths: Mapping[str, tuple[str, ...]] = field(default_factory=lambda: MappingProxyType({}))

    def installation_plan(self, system: str | None = None) -> InstallPlan:
        """Return the reviewed plan for a supported platform."""
        normalized = normalize_system(system or platform.system())
        try:
            return self.install_plans[normalized]
        except KeyError:
            raise ValueError(f"{self.name!r} is not supported on {normalized!r}") from None

    def supports(self, system: str | None = None) -> bool:
        """Return whether this tool has an installation plan for a platform."""
        try:
            return normalize_system(system or platform.system()) in self.install_plans
        except ValueError:
            return False


@dataclass(frozen=True)
class ToolStatus:
    """Observable result of checking a single tool."""

    name: str
    minimum_version: str
    installed: bool
    version: str | None
    supported: bool
    source: str
    error: str | None = None


def normalize_system(system: str) -> str:
    """Normalize Python platform names to the harness vocabulary."""
    aliases = {"linux": "linux", "windows": "windows", "darwin": "macos"}
    try:
        return aliases[system.lower()]
    except KeyError:
        raise ValueError(f"Unsupported platform: {system!r}") from None


TOOLS = (
    ToolSpec(
        "uv",
        "uv",
        "0.11.0",
        "https://docs.astral.sh/uv/getting-started/installation/",
        MappingProxyType(
            {
                "linux": InstallPlan(("curl -LsSf https://astral.sh/uv/0.12.1/install.sh | sh",)),
                "macos": InstallPlan(("curl -LsSf https://astral.sh/uv/0.12.1/install.sh | sh",)),
                "windows": InstallPlan(
                    ('powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.12.1/install.ps1 | iex"',)
                ),
            }
        ),
    ),
    ToolSpec(
        "opencode",
        "opencode",
        "1.18.13",
        "https://opencode.ai/en/docs",
        MappingProxyType(
            {
                "linux": InstallPlan(("npm install -g opencode-ai@1.18.13",)),
                "macos": InstallPlan(("npm install -g opencode-ai@1.18.13",)),
                "windows": InstallPlan(("npm install -g opencode-ai@1.18.13",)),
            }
        ),
    ),
    ToolSpec(
        "jq",
        "jq",
        "1.8.2",
        "https://github.com/jqlang/jq/releases/tag/jq-1.8.2",
        MappingProxyType(
            {
                "linux": InstallPlan(
                    (
                        "curl -fL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o jq",
                        "echo 'b1c22172dd303f3be49e935aa56aa48a8b7a46e0bc838b4997d3bb451495870f  jq' | sha256sum -c -",
                        "mkdir -p ~/.local/bin",
                        "install -m 0755 jq ~/.local/bin/jq",
                    )
                ),
                "windows": InstallPlan(
                    (
                        "Invoke-WebRequest https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-windows-amd64.exe -OutFile jq.exe",
                        "if ((Get-FileHash jq.exe -Algorithm SHA256).Hash -ne 'A6FC67FEDAF9128A3309A1E2EBB8B986AECCF70122EE46D2CB4849E423F0C627') { throw 'Checksum inválido' }",
                    )
                ),
                "macos": InstallPlan(
                    (
                        'set -eu; case "$(uname -m)" in arm64) asset=jq-macos-arm64; sum=2d75340ba57a4b4b4c8708a21c2dc8e958a48aaa8bba13b27f77f6e4c0eca07e ;; x86_64) asset=jq-macos-amd64; sum=e94b266e3c26690550006abe63152b782280f4e14374accdf04cbde844f00bc0 ;; *) echo \'Arquitectura no soportada\' >&2; exit 1 ;; esac; curl -fL "https://github.com/jqlang/jq/releases/download/jq-1.8.2/$asset" -o jq; echo "$sum  jq" | shasum -a 256 -c -; mkdir -p ~/.local/bin; install -m 0755 jq ~/.local/bin/jq',
                    )
                ),
            }
        ),
    ),
    ToolSpec(
        "trello-cli",
        "trello-cli",
        "0.1.1",
        "https://github.com/hammashamzah/trello-cli/releases/tag/v0.1.1",
        MappingProxyType(
            {
                "linux": InstallPlan(
                    (
                        (
                            "set -eu; d=$(mktemp -d); trap 'rm -rf \"$d\"' EXIT; "
                            "curl -fL https://github.com/hammashamzah/trello-cli/releases/download/v0.1.1/"
                            'trello-cli_0.1.1_linux_amd64.tar.gz -o "$d/trello-cli.tar.gz"; '
                            "echo '3513723097cae8b169e477c4a9c12d5b1057b6eef99da6eadd5e6a33753a19de  $d/trello-cli.tar.gz' "
                            '| sha256sum -c -; tar -xzf "$d/trello-cli.tar.gz" -C "$d" trello-cli; '
                            'mkdir -p "$HOME/.local/bin"; install -m 0755 "$d/trello-cli" "$HOME/.local/bin/trello-cli"'
                        ),
                    )
                ),
                "windows": InstallPlan(
                    (
                        (
                            "$d = Join-Path $env:TEMP 'trello-cli.zip'; "
                            "Invoke-WebRequest https://github.com/hammashamzah/trello-cli/releases/download/v0.1.1/"
                            "trello-cli_0.1.1_windows_amd64.zip -OutFile $d; "
                            "if ((Get-FileHash $d -Algorithm SHA256).Hash -ne '5B7D532005ED62C1D93B704969A86007834AB10B9C56457FB352692823CE7EF1') "
                            "{ throw 'Checksum inválido' }; $bin = Join-Path $HOME '.local\\bin'; New-Item -ItemType Directory -Force $bin; "
                            "Expand-Archive $d -DestinationPath $bin -Force"
                        ),
                    )
                ),
            }
        ),
    ),
    ToolSpec(
        "opencode-desktop",
        None,
        "1.18.13",
        "https://opencode.ai/download",
        MappingProxyType(
            {
                "linux": InstallPlan(
                    (
                        (
                            "set -eu; d=$(mktemp -d); trap 'rm -rf \"$d\"' EXIT; "
                            "if command -v dpkg >/dev/null 2>&1; then "
                            "asset=opencode-desktop-linux-amd64.deb; "
                            "sum=125b625886a841f9c8fd9e402f8f1bf8b14a6e08446d313bc0a0dfc693335697; "
                            "manager=deb; "
                            "elif command -v rpm >/dev/null 2>&1; then "
                            "asset=opencode-desktop-linux-x86_64.rpm; "
                            "sum=cc7e557c740fae9a6299dddd0737ad4240e854ce61e45afc015af0e181ad9a94; "
                            "manager=rpm; "
                            "else echo 'No se encontró dpkg ni rpm; instalá OpenCode Desktop manualmente.' >&2; exit 1; fi; "
                            'curl -fL "https://github.com/anomalyco/opencode/releases/download/v1.18.13/$asset" '
                            '-o "$d/$asset"; echo "$sum  $d/$asset" | sha256sum -c -; '
                            'if [ "$manager" = deb ]; then sudo dpkg -i "$d/$asset"; '
                            'else sudo rpm -Uvh "$d/$asset"; fi'
                        ),
                    )
                ),
                "windows": InstallPlan(
                    (
                        (
                            'powershell -NoProfile -ExecutionPolicy Bypass -Command "$d = Join-Path $env:TEMP '
                            "'opencode-desktop-win-x64.exe'; Invoke-WebRequest -Uri "
                            "https://github.com/anomalyco/opencode/releases/download/v1.18.13/"
                            "opencode-desktop-win-x64.exe -OutFile $d; if ((Get-FileHash $d -Algorithm SHA256).Hash "
                            "-ne '3D1796DAA0762EC49CDB27F8418B8E0D2DAFB37D89DD4EA766B42BDD7CD6D260') "
                            "{ throw 'Checksum inválido' }; Start-Process -FilePath $d -Wait\""
                        ),
                    )
                ),
            }
        ),
        MappingProxyType(
            {
                "linux": ("/opt/OpenCode/ai.opencode.desktop", "/usr/bin/ai.opencode.desktop"),
                "windows": (
                    "{localappdata}/Programs/OpenCode/OpenCode.exe",
                    "{programfiles}/OpenCode/OpenCode.exe",
                ),
            }
        ),
    ),
)
TOOLS_BY_NAME = MappingProxyType({tool.name: tool for tool in TOOLS})


def version_at_least(actual: str, minimum: str) -> bool:
    """Compare numeric version prefixes without assuming a tool's suffix format."""

    def numbers(value: str) -> tuple[int, ...]:
        return tuple(int(part) for part in re.findall(r"\d+", value))

    current, required = numbers(actual), numbers(minimum)
    if not current:
        return False
    return current + (0,) * max(0, len(required) - len(current)) >= required


def _version_command(spec: ToolSpec) -> list[str]:
    if spec.command is None:
        raise ValueError(f"{spec.name!r} no tiene un comando de versión")
    return [spec.command, "--version"]


def _detection_path(spec: ToolSpec) -> Path | None:
    """Return the first known application path that exists on this platform."""
    try:
        system = normalize_system(platform.system())
    except ValueError:
        return None
    replacements = {
        "{localappdata}": os.environ.get("LOCALAPPDATA", ""),
        "{programfiles}": os.environ.get("PROGRAMFILES", ""),
    }
    for raw_value in spec.detection_paths.get(system, ()):
        value = raw_value
        for placeholder, replacement in replacements.items():
            value = value.replace(placeholder, replacement)
        path = Path(value).expanduser()
        if path.is_file():
            return path
    return None


def inspect_tool(
    spec: ToolSpec,
    *,
    run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> ToolStatus:
    """Check a tool without changing the host system."""
    supported = spec.supports()
    if spec.command is None:
        path = _detection_path(spec)
        if path is None:
            return ToolStatus(
                spec.name,
                spec.minimum_version,
                False,
                None,
                supported,
                spec.source,
                "not found in expected locations",
            )
        return ToolStatus(spec.name, spec.minimum_version, True, None, supported, spec.source)
    if shutil.which(spec.command) is None:
        return ToolStatus(spec.name, spec.minimum_version, False, None, supported, spec.source, "not found in PATH")
    try:
        result = run(_version_command(spec), capture_output=True, text=True, check=False, timeout=10)
    except (OSError, subprocess.SubprocessError) as error:
        return ToolStatus(spec.name, spec.minimum_version, False, None, supported, spec.source, str(error))
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0:
        return ToolStatus(
            spec.name,
            spec.minimum_version,
            False,
            None,
            supported,
            spec.source,
            output or "version command failed",
        )
    installed = version_at_least(output, spec.minimum_version)
    return ToolStatus(
        spec.name,
        spec.minimum_version,
        installed,
        output,
        supported,
        spec.source,
        None if installed else "version is too old",
    )


def inspect_tools() -> list[ToolStatus]:
    """Inspect every core tool in a deterministic order."""
    return [inspect_tool(spec) for spec in TOOLS]


def installation_plan(spec: ToolSpec, system: str | None = None) -> tuple[str, ...]:
    """Compatibility wrapper for callers that need only the command sequence."""
    return spec.installation_plan(system).commands


def tool_status_json() -> str:
    """Encode inspection results for scripts and the setup skill."""
    return json.dumps([asdict(status) for status in inspect_tools()], ensure_ascii=False)


def install_tool(spec: ToolSpec, *, system: str | None = None, dry_run: bool = False) -> None:
    """Run the reviewed plan only after the caller received explicit consent."""
    for command in installation_plan(spec, system):
        print(f"Install: {command}")
        if not dry_run:
            subprocess.run(command, shell=True, check=True)  # noqa: S602
