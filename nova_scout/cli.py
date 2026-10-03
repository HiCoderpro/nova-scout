"""Command-line interface for NOVA Scout."""

from __future__ import annotations

import argparse

from nova_scout.ideas.repository import IdeaRepository
from nova_scout.ideas.service import IdeaService
from nova_scout.evidence.repository import EvidenceRepository
from nova_scout.research.service import ResearchService
from nova_scout.sources.mock import MockSource


VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    """Build the NOVA Scout command-line parser."""
    parser = argparse.ArgumentParser(
        prog="nova",
        description="NOVA Scout — Niche Opportunity & Validation Analyzer",
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

    idea_parser = subparsers.add_parser(
        "idea",
        help="Manage product ideas.",
    )

    idea_subparsers = idea_parser.add_subparsers(
        dest="idea_command",
        title="idea commands",
    )

    add_parser = idea_subparsers.add_parser(
        "add",
        help="Add a new product idea.",
    )
    add_parser.add_argument(
        "name",
        help="Idea name.",
    )
    add_parser.add_argument(
        "--description",
        default="",
        help="Idea description.",
    )
    add_parser.add_argument(
        "--niche",
        default="",
        help="Target niche.",
    )
    add_parser.add_argument(
        "--target-market",
        default="",
        help="Target market.",
    )
    add_parser.add_argument(
        "--currency",
        default="USD",
        help="Currency code.",
    )

    idea_subparsers.add_parser(
        "list",
        help="List product ideas.",
    )

    get_parser = idea_subparsers.add_parser(
        "get",
        help="Show a product idea.",
    )
    get_parser.add_argument(
        "idea_id",
        help="Idea ID.",
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan an opportunity.",
    )
    scan_parser.add_argument(
        "idea_id",
        help="Idea ID.",
    )
    scan_parser.add_argument(
        "--query",
        default=None,
        help="Research query. Defaults to the idea name.",
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


def _idea_service() -> IdeaService:
    return IdeaService(IdeaRepository())


def _research_service() -> ResearchService:
    return ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(),
    )


def _handle_scan(args: argparse.Namespace) -> None:
    idea_service = _idea_service()
    research_service = _research_service()

    idea = idea_service.get(args.idea_id)

    if idea is None:
        print(f"Idea not found: {args.idea_id}")
        return

    query = args.query or idea.name

    evidences = research_service.research(
        idea_id=idea.id,
        query=query,
    )

    print(f"Scan completed for idea {idea.id}")
    print(f"{len(evidences)} evidence collected")


def _handle_idea(args: argparse.Namespace) -> None:
    service = _idea_service()

    if args.idea_command == "add":
        idea = service.create(
            name=args.name,
            description=args.description,
            niche=args.niche,
            target_market=args.target_market,
            currency=args.currency,
        )

        print(f"Created idea {idea.id}: {idea.name}")
        return

    if args.idea_command == "list":
        ideas = service.list()

        if not ideas:
            print("No ideas found.")
            return

        for idea in ideas:
            print(f"{idea.id}  {idea.name}  [{idea.status}]")
        return

    if args.idea_command == "get":
        idea = service.get(args.idea_id)

        if idea is None:
            print(f"Idea not found: {args.idea_id}")
            return

        print(f"ID: {idea.id}")
        print(f"Name: {idea.name}")
        print(f"Description: {idea.description}")
        print(f"Niche: {idea.niche}")
        print(f"Target market: {idea.target_market}")
        print(f"Currency: {idea.currency}")
        print(f"Status: {idea.status}")
        print(f"Created: {idea.created_at.isoformat()}")
        return

    print("Usage: nova idea {add,list,get}")


def main() -> None:
    """Run the NOVA Scout CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "idea":
        _handle_idea(args)
        return

    if args.command == "scan":
        _handle_scan(args)
        return

    if args.command == "status":
        print(f"NOVA Scout {VERSION}")
        print("Command: status")
        return

    print(f"NOVA Scout {VERSION}")
    print(f"Command: {args.command}")


if __name__ == "__main__":
    main()
