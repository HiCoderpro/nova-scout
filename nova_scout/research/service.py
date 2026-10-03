from __future__ import annotations

from nova_scout.evidence.classifier import EvidenceClassifier
from nova_scout.evidence.models import Evidence
from nova_scout.evidence.repository import EvidenceRepository
from nova_scout.sources.base import Source


class ResearchService:
    def __init__(
        self,
        source: Source,
        evidence_repository: EvidenceRepository,
        classifier: EvidenceClassifier | None = None,
    ):
        self.source = source
        self.evidence_repository = evidence_repository
        self.classifier = classifier or EvidenceClassifier()

    def research(
        self,
        idea_id: str,
        query: str,
    ) -> list[Evidence]:
        query = query.strip()

        if not idea_id.strip():
            raise ValueError("Idea ID cannot be empty.")

        if not query:
            raise ValueError("Research query cannot be empty.")

        results = self.source.fetch(query)

        evidences = []

        for result in results:
            evidence = Evidence(
                idea_id=idea_id,
                source=result.source,
                source_type=result.source_type,
                title=result.title,
                url=result.url,
                content=result.content,
                value=result.value,
                metadata=result.metadata.copy(),
            )

            evidence = self.classifier.classify(evidence)

            evidences.append(
                self.evidence_repository.save(evidence)
            )

        return evidences
