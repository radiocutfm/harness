"""Command-line interface for Fierro Agents Harness."""

from __future__ import annotations

import argparse

from . import __version__
from .installer import install


def main() -> int:
    """Run the harness command-line interface."""
    parser = argparse.ArgumentParser(prog="fierro-harness")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    install_parser = subparsers.add_parser("install", help="Install or reconcile the harness")
    install_parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.command == "install":
        print(f"Fierro-harness {__version__}: {'dry-run' if args.dry_run else 'install'}")
        return install(dry_run=args.dry_run)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
