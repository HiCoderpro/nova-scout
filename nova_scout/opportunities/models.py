from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class OpportunityProfile:
    idea_id: str
    demand_signals: list[str] = field(default_factory=list)
    competition_signals: list[str] = field(default_factory=list)
    pricing_signals: list[str] = field(default_factory=list)
    market_signals: list[str] = field(default_factory=list)
    confidence: str = "UNKNOWN"
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
