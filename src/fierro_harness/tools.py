"""Detection and opt-in installation plans for harness command-line tools."""

from __future__ import annotations

import json
import platform
import re
import shutil
import subprocess
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class InstallPlan:
    """Reviewed commands for installing one tool on one platform."""

    commands: tuple[str, ...]


@dataclass(frozen=True)
class ToolSpec:
    """The stable contract for a command used by one or more skills."""

    name: str
    command: str
    minimum_version: str
    source: str
    install_plans: Mapping[str, InstallPlan]

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
                        "set -eu; case \"$(uname -m)\" in arm64) asset=jq-macos-arm64; sum=2d75340ba57a4b4b4c8708a21c2dc8e958a48aaa8bba13b27f77f6e4c0eca07e ;; x86_64) asset=jq-macos-amd64; sum=e94b266e3c26690550006abe63152b782280f4e14374accdf04cbde844f00bc0 ;; *) echo 'Arquitectura no soportada' >&2; exit 1 ;; esac; curl -fL \"https://github.com/jqlang/jq/releases/download/jq-1.8.2/$asset\" -o jq; echo \"$sum  jq\" | shasum -a 256 -c -; mkdir -p ~/.local/bin; install -m 0755 jq ~/.local/bin/jq",
                    )
                ),
            }
        ),
    ),
)
TOOLS_BY_NAME = MappingProxyType({tool.name: tool for tool in TOOLS})


def version_at_least(actual: str, minimum: str) -> bool:
    """Compare numeric version prefixes without assuming a tool's suffix format."""
    numbers = lambda value: tuple(int(part) for part in re.findall(r"\d+", value))
    current, required = numbers(actual), numbers(minimum)
    if not current:
        return False
    return current + (0,) * max(0, len(required) - len(current)) >= required


def _version_command(spec: ToolSpec) -> list[str]:
    return [spec.command, "--version"]


def inspect_tool(spec: ToolSpec, *, run: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> ToolStatus:
    """Check a tool without changing the host system."""
    supported = spec.supports()
    if shutil.which(spec.command) is None:
        return ToolStatus(spec.name, spec.minimum_version, False, None, supported, spec.source, "not found in PATH")
    try:
        result = run(_version_command(spec), capture_output=True, text=True, check=False, timeout=10)
    except (OSError, subprocess.SubprocessError) as error:
        return ToolStatus(spec.name, spec.minimum_version, False, None, supported, spec.source, str(error))
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0:
        return ToolStatus(spec.name, spec.minimum_version, False, None, supported, spec.source, output or "version command failed")
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
