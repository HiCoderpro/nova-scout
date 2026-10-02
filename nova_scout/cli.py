"""Command-line interface for NOVA Scout."""

from __future__ import annotations

import argparse


VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    """Build the NOVA Scout command-line parser."""
    parser = argparse.ArgumentParser(
        prog="nova",
        description=(
            "NOVA Scout — Niche Opportunity & Validation Analyzer"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
    )

    subparsers.add_parser(
        "status",
        help="Show NOVA Scout system status.",
    )

    subparsers.add_parser(
        "idea",
        help="Manage product ideas.",
    )

    subparsers.add_parser(
        "scan",
        help="Scan an opportunity.",
    )

    subparsers.add_parser(
        "report",
        help="Generate an opportunity report.",
    )

    subparsers.add_parser(
        "compare",
        help="Compare opportunities.",
    )

    return parser


def main() -> None:
    """Run the NOVA Scout CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    print(f"NOVA Scout {VERSION}")
    print(f"Command: {args.command}")


if __name__ == "__main__":
    main()
