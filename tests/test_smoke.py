import pytest

from nova_scout.cli import VERSION, build_parser


def test_nova_scout_imports():
    import nova_scout

    assert nova_scout is not None


def test_cli_parser():
    parser = build_parser()

    args = parser.parse_args(["status"])

    assert args.command == "status"


def test_cli_version():
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--version"])

    assert exc_info.value.code == 0


def test_cli_commands():
    parser = build_parser()

    expected_commands = {
        "status",
        "idea",
        "scan",
        "report",
        "compare",
    }

    for command in expected_commands:
        args = parser.parse_args([command])
        assert args.command == command
