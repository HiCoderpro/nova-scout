from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Evidence:
    idea_id: str
    source: str
    source_type: str
    title: str
    url: str
    content: str = ""
    value: object = None
    metadata: dict = field(default_factory=dict)
    id: str | None = None
    collected_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
