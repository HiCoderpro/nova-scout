from __future__ import annotations

from nova_scout.evidence.models import Evidence
from nova_scout.evidence.repository import EvidenceRepository
from nova_scout.research.service import ResearchService
from nova_scout.sources.base import Source


class ScanService:
    def __init__(
        self,
        source: Source,
        evidence_repository: EvidenceRepository,
    ):
        self.research_service = ResearchService(
            source=source,
            evidence_repository=evidence_repository,
        )

    def scan(
        self,
        idea_id: str,
        query: str,
    ) -> list[Evidence]:
        return self.research_service.research(
            idea_id=idea_id,
            query=query,
        )
