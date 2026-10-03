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

    command_args = {
        "status": ["status"],
        "idea": ["idea"],
        "scan": ["scan", "001"],
        "report": ["report"],
        "compare": ["compare"],
    }

    for command in expected_commands:
        args = parser.parse_args(command_args[command])
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


def test_mock_source_returns_evidence():
    from nova_scout.sources.mock import MockSource

    source = MockSource()

    results = source.search("invoice generator")

    assert len(results) == 1
    assert results[0].source == "mock"
    assert results[0].query == "invoice generator"
    assert results[0].title == "Mock result for invoice generator"
    assert results[0].url == "https://example.com/mock"
    assert "invoice generator" in results[0].content


def test_evidence_model():
    from nova_scout.evidence.models import Evidence

    evidence = Evidence(
        idea_id="001",
        source="mock",
        source_type="mock",
        title="Example Result",
        url="https://example.com",
        content="Example evidence",
        value=42,
    )

    assert evidence.id is None
    assert evidence.idea_id == "001"
    assert evidence.source == "mock"
    assert evidence.source_type == "mock"
    assert evidence.title == "Example Result"
    assert evidence.url == "https://example.com"
    assert evidence.content == "Example evidence"
    assert evidence.value == 42
    assert evidence.metadata == {}
    assert evidence.collected_at.tzinfo is not None


def test_evidence_repository(tmp_path):
    from nova_scout.evidence.models import Evidence
    from nova_scout.evidence.repository import EvidenceRepository

    repository = EvidenceRepository(tmp_path / "evidence.json")

    evidence = repository.save(
        Evidence(
            idea_id="001",
            source="mock",
            source_type="mock",
            title="Example Result",
            url="https://example.com",
            content="Example evidence",
            value=42,
        )
    )

    assert evidence.id == "001"

    loaded = repository.get("001")

    assert loaded is not None
    assert loaded.idea_id == "001"
    assert loaded.title == "Example Result"

    evidences = repository.list()

    assert len(evidences) == 1


def test_evidence_repository_filters_by_idea(tmp_path):
    from nova_scout.evidence.models import Evidence
    from nova_scout.evidence.repository import EvidenceRepository

    repository = EvidenceRepository(tmp_path / "evidence.json")

    repository.save(
        Evidence(
            idea_id="001",
            source="mock",
            source_type="mock",
            title="Evidence A",
            url="https://example.com/a",
        )
    )

    repository.save(
        Evidence(
            idea_id="002",
            source="mock",
            source_type="mock",
            title="Evidence B",
            url="https://example.com/b",
        )
    )

    evidences = repository.list(idea_id="001")

    assert len(evidences) == 1
    assert evidences[0].idea_id == "001"
    assert evidences[0].title == "Evidence A"


def test_research_service_collects_evidence(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    repository = EvidenceRepository(tmp_path / "evidence.json")

    service = ResearchService(
        source=MockSource(),
        evidence_repository=repository,
    )

    evidences = service.research(
        idea_id="001",
        query="invoice generator",
    )

    assert len(evidences) == 1
    assert evidences[0].id == "001"
    assert evidences[0].idea_id == "001"
    assert evidences[0].source == "mock"
    assert evidences[0].title == "Mock result for invoice generator"
    assert "invoice generator" in evidences[0].content

    stored = repository.list(idea_id="001")

    assert len(stored) == 1
    assert stored[0].id == "001"


def test_research_service_rejects_empty_query(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    service = ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(
            tmp_path / "evidence.json"
        ),
    )

    try:
        service.research("001", "   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Research query cannot be empty."


def test_research_service_rejects_empty_idea_id(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    service = ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(
            tmp_path / "evidence.json"
        ),
    )

    try:
        service.research("   ", "invoice generator")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Idea ID cannot be empty."


def test_research_service_collects_evidence(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    repository = EvidenceRepository(tmp_path / "evidence.json")

    service = ResearchService(
        source=MockSource(),
        evidence_repository=repository,
    )

    evidences = service.research(
        idea_id="001",
        query="invoice generator",
    )

    assert len(evidences) == 1
    assert evidences[0].id == "001"
    assert evidences[0].idea_id == "001"
    assert evidences[0].source == "mock"
    assert evidences[0].title == "Mock result for invoice generator"
    assert "invoice generator" in evidences[0].content

    stored = repository.list(idea_id="001")

    assert len(stored) == 1
    assert stored[0].id == "001"


def test_research_service_rejects_empty_query(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    service = ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(
            tmp_path / "evidence.json"
        ),
    )

    try:
        service.research("001", "   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Research query cannot be empty."


def test_research_service_rejects_empty_idea_id(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    service = ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(
            tmp_path / "evidence.json"
        ),
    )

    try:
        service.research("   ", "invoice generator")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Idea ID cannot be empty."


def test_research_service_creates_evidence(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    repository = EvidenceRepository(tmp_path / "evidence.json")
    service = ResearchService(
        source=MockSource(),
        evidence_repository=repository,
    )

    evidences = service.research(
        idea_id="001",
        query="invoice generator",
    )

    assert len(evidences) == 1

    evidence = evidences[0]

    assert evidence.id == "001"
    assert evidence.idea_id == "001"
    assert evidence.source == "mock"
    assert evidence.source_type == "mock"
    assert evidence.title == "Mock result for invoice generator"
    assert evidence.value == 42
    assert "invoice generator" in evidence.content


def test_research_service_persists_evidence(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    path = tmp_path / "evidence.json"

    service = ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(path),
    )

    service.research(
        idea_id="001",
        query="invoice generator",
    )

    repository = EvidenceRepository(path)

    evidences = repository.list("001")

    assert len(evidences) == 1
    assert evidences[0].id == "001"
    assert evidences[0].idea_id == "001"


def test_research_service_rejects_empty_input(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.service import ResearchService
    from nova_scout.sources.mock import MockSource

    service = ResearchService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(
            tmp_path / "evidence.json"
        ),
    )

    try:
        service.research("", "invoice generator")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Idea ID cannot be empty."

    try:
        service.research("001", "   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Research query cannot be empty."


def test_scan_service(tmp_path):
    from nova_scout.evidence.repository import EvidenceRepository
    from nova_scout.research.scan import ScanService
    from nova_scout.sources.mock import MockSource

    service = ScanService(
        source=MockSource(),
        evidence_repository=EvidenceRepository(
            tmp_path / "evidence.json"
        ),
    )

    evidences = service.scan(
        idea_id="001",
        query="invoice generator",
    )

    assert len(evidences) == 1
    assert evidences[0].idea_id == "001"
    assert evidences[0].source == "mock"


def test_cli_scan_creates_evidence(tmp_path, monkeypatch, capsys):
    from nova_scout import cli
    from nova_scout.evidence.repository import EvidenceRepository

    monkeypatch.chdir(tmp_path)

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "idea", "add", "Invoice Generator"],
    )
    cli.main()

    monkeypatch.setattr(
        "sys.argv",
        ["nova", "scan", "001"],
    )
    cli.main()

    output = capsys.readouterr().out

    assert "Scan completed for idea 001" in output
    assert "1 evidence collected" in output

    repository = EvidenceRepository(tmp_path / "data" / "evidence.json")
    evidences = repository.list("001")

    assert len(evidences) == 1
    assert evidences[0].source == "mock"
    assert evidences[0].idea_id == "001"
    assert "Invoice Generator" in evidences[0].content
