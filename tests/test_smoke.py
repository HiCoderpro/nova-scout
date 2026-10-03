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


def test_idea_model():
    from nova_scout.ideas.models import Idea

    idea = Idea(name="Example Product")

    assert idea.name == "Example Product"
    assert idea.currency == "USD"
    assert idea.status == "NEW"
    assert idea.id is None


def test_idea_repository(tmp_path):
    from nova_scout.ideas.models import Idea
    from nova_scout.ideas.repository import IdeaRepository

    repository = IdeaRepository(tmp_path / "ideas.json")

    idea = repository.save(Idea(name="Example Product"))

    assert idea.id == "001"

    loaded = repository.get("001")

    assert loaded is not None
    assert loaded.name == "Example Product"

    ideas = repository.list()

    assert len(ideas) == 1


def test_idea_service_create(tmp_path):
    from nova_scout.ideas.repository import IdeaRepository
    from nova_scout.ideas.service import IdeaService

    service = IdeaService(
        IdeaRepository(tmp_path / "ideas.json")
    )

    idea = service.create(
        "  Example Product  ",
        description="  A useful product  ",
        niche="  Freelancers  ",
        target_market="  International  ",
        currency="usd",
    )

    assert idea.id == "001"
    assert idea.name == "Example Product"
    assert idea.description == "A useful product"
    assert idea.niche == "Freelancers"
    assert idea.target_market == "International"
    assert idea.currency == "USD"


def test_idea_service_rejects_empty_name(tmp_path):
    from nova_scout.ideas.repository import IdeaRepository
    from nova_scout.ideas.service import IdeaService

    service = IdeaService(
        IdeaRepository(tmp_path / "ideas.json")
    )

    try:
        service.create("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Idea name cannot be empty."


def test_idea_service_list(tmp_path):
    from nova_scout.ideas.repository import IdeaRepository
    from nova_scout.ideas.service import IdeaService

    service = IdeaService(
        IdeaRepository(tmp_path / "ideas.json")
    )

    service.create("Product A")
    service.create("Product B")

    ideas = service.list()

    assert len(ideas) == 2
    assert ideas[0].id == "001"
    assert ideas[1].id == "002"
def test_cli_idea_add(tmp_path, monkeypatch, capsys):
    from nova_scout import cli

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "add", "Test Product"],
    )

    cli.main()

    output = capsys.readouterr().out

    assert "Created idea 001: Test Product" in output


def test_cli_idea_list(tmp_path, monkeypatch, capsys):
    from nova_scout import cli

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "add", "Product A"],
    )
    cli.main()

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "add", "Product B"],
    )
    cli.main()

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "list"],
    )
    cli.main()

    output = capsys.readouterr().out

    assert "001  Product A  [NEW]" in output
    assert "002  Product B  [NEW]" in output


def test_cli_idea_get(tmp_path, monkeypatch, capsys):
    from nova_scout import cli

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "add", "Test Product"],
    )
    cli.main()

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "get", "001"],
    )
    cli.main()

    output = capsys.readouterr().out

    assert "ID: 001" in output
    assert "Name: Test Product" in output
    assert "Status: NEW" in output


def test_source_result():
    from nova_scout.sources.base import SourceResult

    result = SourceResult(
        source="test",
        source_type="mock",
        query="example",
        title="Example Result",
        url="https://example.com",
        value=42,
    )

    assert result.source == "test"
    assert result.source_type == "mock"
    assert result.query == "example"
    assert result.title == "Example Result"
    assert result.value == 42
    assert result.metadata == {}


def test_source_contract():
    from nova_scout.sources.base import Source

    source = Source()

    assert source.name == "base"
    assert source.source_type == "unknown"

    try:
        source.fetch("example")
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass
