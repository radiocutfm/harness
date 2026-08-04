# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Bootstrap entry point; reconciliation is tracked in the implementation issues."""

from __future__ import annotations

import argparse
def main() -> None:
    parser = argparse.ArgumentParser(description="Install or repair Fierro Agents Harness")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    mode = "dry-run" if args.dry_run else "plan"
    print(f"harness 0.1.0: {mode}")


if __name__ == "__main__":
    main()
