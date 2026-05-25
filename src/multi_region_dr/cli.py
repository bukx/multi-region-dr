"""Command-line entrypoint for the DR simulator."""

from __future__ import annotations

import argparse
import json

from .orchestrator import DRManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Multi-region DR simulator")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show current DR status")

    failover = subparsers.add_parser("failover", help="Promote secondary region")
    failover.add_argument("--reason", default="manual drill")

    subparsers.add_parser("recover", help="Restore traffic to the primary region")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    manager = DRManager.from_file(args.config)

    if args.command == "status":
        payload = manager.status()
    elif args.command == "failover":
        payload = manager.failover(args.reason)
    else:
        payload = manager.recover_primary()

    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
