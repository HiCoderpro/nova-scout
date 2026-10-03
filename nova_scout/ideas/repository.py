from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .models import Idea


class IdeaRepository:
    def __init__(self, path: str | Path = "data/ideas.json"):
        self.path = Path(path)

    def save(self, idea: Idea) -> Idea:
        ideas = self.list()

        if idea.id is None:
            idea.id = self._next_id(ideas)

        existing_index = next(
            (index for index, item in enumerate(ideas) if item.id == idea.id),
            None,
        )

        if existing_index is None:
            ideas.append(idea)
        else:
            ideas[existing_index] = idea

        self._write(ideas)
        return idea

    def list(self) -> list[Idea]:
        if not self.path.exists():
            return []

        raw = json.loads(self.path.read_text(encoding="utf-8"))

        return [
            Idea(
                id=item["id"],
                name=item["name"],
                description=item.get("description", ""),
                niche=item.get("niche", ""),
                target_market=item.get("target_market", ""),
                currency=item.get("currency", "USD"),
                status=item.get("status", "NEW"),
                created_at=datetime.fromisoformat(
                    item["created_at"]
                ),
            )
            for item in raw
        ]

    def get(self, idea_id: str) -> Idea | None:
        return next(
            (idea for idea in self.list() if idea.id == idea_id),
            None,
        )

    def _next_id(self, ideas: list[Idea]) -> str:
        if not ideas:
            return "001"

        numbers = [
            int(idea.id)
            for idea in ideas
            if idea.id and idea.id.isdigit()
        ]

        return f"{max(numbers, default=0) + 1:03d}"

    def _write(self, ideas: list[Idea]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        data = []

        for idea in ideas:
            item = asdict(idea)
            item["created_at"] = idea.created_at.isoformat()
            data.append(item)

        self.path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
