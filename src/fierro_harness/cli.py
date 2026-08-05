"""Interfaz de línea de comandos de Fierro Agents Harness."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Annotated

import typer

from . import __version__
from .installer import install as reconcile_install
from .tools import TOOLS, inspect_tools, install_tool, installation_plan

app = typer.Typer(
    add_completion=False,
    help="Instala y prepara las herramientas de Fierro Harness.",
    rich_markup_mode=None,
)


def version_callback(value: bool) -> None:
    """Muestra la versión instalada antes de procesar el comando."""
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def root(
    version: Annotated[
        bool,
        typer.Option("--version", callback=version_callback, is_eager=True, help="Muestra la versión del harness."),
    ] = False,
) -> None:
    """Instala, inspecciona y prepara los componentes de Fierro Harness."""


@app.command()
def install(
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Muestra los cambios sin aplicarlos.")] = False,
) -> None:
    """Instala o reconcilia el harness."""
    typer.echo(f"Fierro-harness {__version__}: {'simulación' if dry_run else 'instalación'}")
    raise typer.Exit(reconcile_install(dry_run=dry_run))


@app.command()
def tools(
    as_json: Annotated[bool, typer.Option("--json", help="Emite JSON.")] = False,
    plan: Annotated[str | None, typer.Option("--plan", help="Muestra un plan de instalación.")] = None,
) -> None:
    """Inspecciona las herramientas de línea de comandos principales."""
    if plan:
        tool = next((item for item in TOOLS if item.name == plan), None)
        if tool is None:
            raise typer.BadParameter(f"herramienta desconocida: {plan}", param_hint="--plan")
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
            state = "correcta" if status.installed else "desactualizada" if status.version else "ausente"
            version = status.version or "-"
            typer.echo(f"{status.name}: {state}; version={version}; minimum={status.minimum_version}")
    raise typer.Exit(0 if all(status.installed for status in statuses) else 1)


@app.command()
def setup(
    install_names: Annotated[
        list[str] | None,
        typer.Option("--install", help="Herramienta a instalar; repetí la opción para varias herramientas."),
    ] = None,
    yes: Annotated[bool, typer.Option("--yes", help="Confirma el plan de instalación mostrado.")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Muestra los comandos sin ejecutarlos.")] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emite JSON.")] = False,
) -> None:
    """Verifica o instala explícitamente herramientas de las skills habilitadas."""
    requested = set(install_names or [])
    unknown = requested - {tool.name for tool in TOOLS} - {"all"}
    if unknown:
        raise typer.BadParameter(f"herramienta desconocida: {min(unknown)}", param_hint="--install")
    statuses = inspect_tools()
    selected = TOOLS if "all" in requested else tuple(tool for tool in TOOLS if tool.name in requested)
    if not selected:
        if as_json:
            typer.echo(json.dumps([asdict(status) for status in statuses], ensure_ascii=False))
        else:
            for status in statuses:
                state = "correcta" if status.installed else "pendiente"
                typer.echo(f"{status.name}: {state}; minimum={status.minimum_version}; source={status.source}")
        raise typer.Exit(0 if all(status.installed for status in statuses) else 1)
    confirmed = yes or os.environ.get("FIERRO_HARNESS_ASSUME_YES") == "1"
    if not confirmed:
        for tool in selected:
            typer.echo(f"{tool.name} ({tool.minimum_version} o posterior):")
            for command in installation_plan(tool):
                typer.echo(f"  {command}")
        typer.echo("Volvé a ejecutar con --yes para confirmar la instalación.")
        typer.echo("En automatizaciones, usá FIERRO_HARNESS_ASSUME_YES=1.")
        raise typer.Exit(1)
    for tool in selected:
        install_tool(tool, dry_run=dry_run)


def main() -> None:
    """Ejecuta la aplicación de Typer."""
    app()
