"""Detection and opt-in installation plans for harness command-line tools."""

from __future__ import annotations

import json
import platform
import re
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ToolSpec:
    """The stable contract for a command used by one or more skills."""

    name: str
    command: str
    minimum_version: str
    source: str


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


TOOLS = (
    ToolSpec("uv", "uv", "0.11.0", "https://docs.astral.sh/uv/getting-started/installation/"),
    ToolSpec("opencode", "opencode", "1.18.13", "https://opencode.ai/en/docs"),
    ToolSpec("jq", "jq", "1.8.2", "https://github.com/jqlang/jq/releases/tag/jq-1.8.2"),
)


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
    if shutil.which(spec.command) is None:
        return ToolStatus(spec.name, spec.minimum_version, False, None, True, spec.source, "not found in PATH")
    try:
        result = run(_version_command(spec), capture_output=True, text=True, check=False, timeout=10)
    except (OSError, subprocess.SubprocessError) as error:
        return ToolStatus(spec.name, spec.minimum_version, False, None, True, spec.source, str(error))
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0:
        return ToolStatus(spec.name, spec.minimum_version, False, None, True, spec.source, output or "version command failed")
    return ToolStatus(
        spec.name,
        spec.minimum_version,
        version_at_least(output, spec.minimum_version),
        output,
        True,
        spec.source,
        None if version_at_least(output, spec.minimum_version) else "version is too old",
    )


def inspect_tools() -> list[ToolStatus]:
    """Inspect every core tool in a deterministic order."""
    return [inspect_tool(spec) for spec in TOOLS]


def installation_plan(spec: ToolSpec, system: str | None = None) -> list[str]:
    """Return only reviewed, user-visible installation commands for a platform."""
    system = (system or platform.system()).lower()
    if spec.name == "uv":
        if system == "windows":
            return ['powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.12.1/install.ps1 | iex"']
        return ["curl -LsSf https://astral.sh/uv/0.12.1/install.sh | sh"]
    if spec.name == "opencode":
        if system == "windows":
            return ["npm install -g opencode-ai"]
        return ["curl -fsSL https://opencode.ai/install | bash"]
    if spec.name == "jq":
        if system == "windows":
            return [
                "Invoke-WebRequest https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-windows-amd64.exe -OutFile jq.exe",
                "(Get-FileHash jq.exe -Algorithm SHA256).Hash -eq 'A6FC67FEDAF9128A3309A1E2EBB8B986AECCF70122EE46D2CB4849E423F0C627'",
            ]
        return [
            "curl -fL https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-linux-amd64 -o jq",
            "echo 'b1c22172dd303f3be49e935aa56aa48a8b7a46e0bc838b4997d3bb451495870f  jq' | sha256sum -c -",
            "install -m 0755 jq ~/.local/bin/jq",
        ]
    raise ValueError(f"Unknown tool: {spec.name}")


def tool_status_json() -> str:
    """Encode inspection results for scripts and the setup skill."""
    return json.dumps([asdict(status) for status in inspect_tools()], ensure_ascii=False)
