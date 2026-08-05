"""Command-line interface for Fierro Agents Harness."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Annotated

import typer

from . import __version__
from .installer import install as reconcile_install
from .tools import TOOLS, inspect_tools, install_tool, installation_plan

app = typer.Typer(add_completion=False, help="Install and prepare Fierro harness tools.", rich_markup_mode=None)


def version_callback(value: bool) -> None:
    """Print the installed harness version before command processing."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def root(
    version: Annotated[
        bool,
        typer.Option("--version", callback=version_callback, is_eager=True, help="Show the harness version."),
    ] = False,
) -> None:
    """Install, inspect, and prepare Fierro harness components."""


@app.command()
def install(
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show changes without applying them.")] = False,
) -> None:
    """Install or reconcile the harness."""
    typer.echo(f"Fierro-harness {__version__}: {'dry-run' if dry_run else 'install'}")
    raise typer.Exit(reconcile_install(dry_run=dry_run))


@app.command()
def tools(
    as_json: Annotated[bool, typer.Option("--json", help="Emit JSON.")] = False,
    plan: Annotated[str | None, typer.Option("--plan", help="Show an installation plan.")] = None,
) -> None:
    """Inspect core command-line tools."""
    if plan:
        tool = next((item for item in TOOLS if item.name == plan), None)
        if tool is None:
            raise typer.BadParameter(f"unknown tool: {plan}", param_hint="--plan")
        try:
            typer.echo("\n".join(installation_plan(tool)))
        except ValueError as error:
            raise typer.BadParameter(str(error), param_hint="--plan") from None
        return

    statuses = inspect_tools()
    if as_json:
        typer.echo(json.dumps([asdict(status) for status in statuses], ensure_ascii=False))
    else:
        for status in statuses:
            state = "ok" if status.installed else "outdated" if status.version else "missing"
            version = status.version or "-"
            typer.echo(f"{status.name}: {state}; version={version}; minimum={status.minimum_version}")
    raise typer.Exit(0 if all(status.installed for status in statuses) else 1)


@app.command()
def setup(
    install_names: Annotated[
        list[str] | None,
        typer.Option("--install", help="Tool to install; repeat the option for multiple tools."),
    ] = None,
    yes: Annotated[bool, typer.Option("--yes", help="Confirm the displayed installation plan.")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show installation commands without running them.")] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit JSON.")] = False,
) -> None:
    """Check or explicitly install tools for enabled skills."""
    requested = set(install_names or [])
    unknown = requested - {tool.name for tool in TOOLS} - {"all"}
    if unknown:
        raise typer.BadParameter(f"unknown tool: {min(unknown)}", param_hint="--install")
    statuses = inspect_tools()
    selected = TOOLS if "all" in requested else tuple(tool for tool in TOOLS if tool.name in requested)
    if not selected:
        if as_json:
            typer.echo(json.dumps([asdict(status) for status in statuses], ensure_ascii=False))
        else:
            for status in statuses:
                state = "ok" if status.installed else "pending"
                typer.echo(f"{status.name}: {state}; minimum={status.minimum_version}; source={status.source}")
        raise typer.Exit(0 if all(status.installed for status in statuses) else 1)
    if not yes:
        for tool in selected:
            typer.echo(f"{tool.name} ({tool.minimum_version} or newer):")
            for command in installation_plan(tool):
                typer.echo(f"  {command}")
        typer.echo("Re-run with --yes to confirm installation.")
        raise typer.Exit(1)
    for tool in selected:
        install_tool(tool, dry_run=dry_run)


def main() -> None:
    """Run the Typer application."""
    app()
