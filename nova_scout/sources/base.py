from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceResult:
    source: str
    source_type: str
    query: str
    title: str
    url: str
    value: Any
    content: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class Source:
    name = "base"
    source_type = "unknown"

    def fetch(self, query: str) -> list[SourceResult]:
        raise NotImplementedError

    def search(self, query: str) -> list[SourceResult]:
        return self.fetch(query)
