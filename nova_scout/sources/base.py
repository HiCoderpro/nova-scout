"""Base contracts for NOVA Scout data sources."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SourceResult:
    """Normalized result returned by a source connector."""

    source: str
    source_type: str
    query: str
    title: str = ""
    url: str = ""
    value: Any = None
    collected_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, Any] = field(default_factory=dict)


class Source:
    """Base contract that every NOVA Scout source must implement."""

    name: str = "base"
    source_type: str = "unknown"

    def fetch(self, query: str) -> list[SourceResult]:
        """Collect raw information for a query."""
        raise NotImplementedError
