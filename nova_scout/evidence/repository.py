from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import Evidence


class EvidenceRepository:
    def __init__(self, path: str | Path = "data/evidence.json"):
        self.path = Path(path)

    def save(self, evidence: Evidence) -> Evidence:
        evidences = self.list()

        if evidence.id is None:
            evidence.id = self._next_id(evidences)

        existing_index = next(
            (
                index
                for index, item in enumerate(evidences)
                if item.id == evidence.id
            ),
            None,
        )

        if existing_index is None:
            evidences.append(evidence)
        else:
            evidences[existing_index] = evidence

        self._write(evidences)
        return evidence

    def list(self, idea_id: str | None = None) -> list[Evidence]:
        if not self.path.exists():
            return []

        raw = json.loads(self.path.read_text(encoding="utf-8"))

        evidences = [
            Evidence(
                id=item["id"],
                idea_id=item["idea_id"],
                source=item["source"],
                source_type=item["source_type"],
                title=item["title"],
                url=item["url"],
                content=item.get("content", ""),
                value=item.get("value"),
                metadata=item.get("metadata", {}),
            )
            for item in raw
        ]

        if idea_id is not None:
            evidences = [
                evidence
                for evidence in evidences
                if evidence.idea_id == idea_id
            ]

        return evidences

    def get(self, evidence_id: str) -> Evidence | None:
        return next(
            (
                evidence
                for evidence in self.list()
                if evidence.id == evidence_id
            ),
            None,
        )

    def _next_id(self, evidences: list[Evidence]) -> str:
        if not evidences:
            return "001"

        numbers = [
            int(evidence.id)
            for evidence in evidences
            if evidence.id and evidence.id.isdigit()
        ]

        return f"{max(numbers, default=0) + 1:03d}"

    def _write(self, evidences: list[Evidence]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        data = []

        for evidence in evidences:
            item = asdict(evidence)
            item["collected_at"] = evidence.collected_at.isoformat()
            data.append(item)

        self.path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
