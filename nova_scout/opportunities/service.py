from __future__ import annotations

from nova_scout.evidence.repository import EvidenceRepository
from nova_scout.opportunities.models import OpportunityProfile
from nova_scout.opportunities.repository import OpportunityProfileRepository


class OpportunityProfileService:
    def __init__(
        self,
        evidence_repository: EvidenceRepository,
        profile_repository: OpportunityProfileRepository,
    ):
        self.evidence_repository = evidence_repository
        self.profile_repository = profile_repository

    def build(self, idea_id: str) -> OpportunityProfile:
        if not idea_id.strip():
            raise ValueError("Idea ID cannot be empty.")

        evidences = self.evidence_repository.list(idea_id)

        demand_signals: list[str] = []
        competition_signals: list[str] = []
        pricing_signals: list[str] = []
        market_signals: list[str] = []

        for evidence in evidences:
            classification = evidence.source_type.strip().lower()

            if classification == "demand":
                demand_signals.append(evidence.content)

            elif classification == "competition":
                competition_signals.append(evidence.content)

            elif classification == "pricing":
                pricing_signals.append(evidence.content)

            elif classification == "market":
                market_signals.append(evidence.content)

        profile = OpportunityProfile(
            idea_id=idea_id,
            demand_signals=demand_signals,
            competition_signals=competition_signals,
            pricing_signals=pricing_signals,
            market_signals=market_signals,
            confidence="UNKNOWN",
        )

        return self.profile_repository.save(profile)
