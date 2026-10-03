from __future__ import annotations

from .base import Source, SourceResult


class MockSource(Source):
    name = "mock"
    source_type = "mock"

    def fetch(self, query: str) -> list[SourceResult]:
        return [
            SourceResult(
                source=self.name,
                source_type=self.source_type,
                query=query,
                title=f"Mock result for {query}",
                url="https://example.com/mock",
                value=42,
                content=(
                    f"This is deterministic mock evidence for the query: {query}"
                ),
            )
        ]
