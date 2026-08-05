"""Command-line interface for Fierro Agents Harness."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from . import __version__
from .installer import install
from .tools import TOOLS, inspect_tools, installation_plan


def main() -> int:
    """Run the harness command-line interface."""
    parser = argparse.ArgumentParser(prog="fierro-harness")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    install_parser = subparsers.add_parser("install", help="Install or reconcile the harness")
    install_parser.add_argument("--dry-run", action="store_true")
    tools_parser = subparsers.add_parser("tools", help="Inspect core command-line tools")
    tools_parser.add_argument("--json", action="store_true", dest="as_json")
    tools_parser.add_argument("--plan", choices=[tool.name for tool in TOOLS])
    args = parser.parse_args()
    if args.command == "install":
        print(f"Fierro-harness {__version__}: {'dry-run' if args.dry_run else 'install'}")
        return install(dry_run=args.dry_run)
    if args.command == "tools":
        if args.plan:
            try:
                print("\n".join(installation_plan(next(tool for tool in TOOLS if tool.name == args.plan))))
            except ValueError as error:
                parser.error(str(error))
            return 0
        statuses = inspect_tools()
        if args.as_json:
            print(json.dumps([asdict(status) for status in statuses], ensure_ascii=False))
        else:
            for status in statuses:
                state = "ok" if status.installed else "outdated" if status.version else "missing"
                version = status.version or "-"
                print(f"{status.name}: {state}; version={version}; minimum={status.minimum_version}")
        return 0 if all(status.installed for status in statuses) else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
