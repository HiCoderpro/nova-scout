from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import OpportunityProfile


class OpportunityProfileRepository:
    def __init__(
        self,
        path: str | Path = "data/opportunity_profiles.json",
    ):
        self.path = Path(path)

    def save(self, profile: OpportunityProfile) -> OpportunityProfile:
        profiles = self.list()

        existing_index = next(
            (
                index
                for index, item in enumerate(profiles)
                if item.idea_id == profile.idea_id
            ),
            None,
        )

        if existing_index is None:
            profiles.append(profile)
        else:
            profiles[existing_index] = profile

        self._write(profiles)
        return profile

    def get(self, idea_id: str) -> OpportunityProfile | None:
        return next(
            (
                profile
                for profile in self.list()
                if profile.idea_id == idea_id
            ),
            None,
        )

    def list(self) -> list[OpportunityProfile]:
        if not self.path.exists():
            return []

        raw = json.loads(
            self.path.read_text(encoding="utf-8")
        )

        return [
            OpportunityProfile(
                idea_id=item["idea_id"],
                demand_signals=item.get("demand_signals", []),
                competition_signals=item.get(
                    "competition_signals", []
                ),
                pricing_signals=item.get(
                    "pricing_signals", []
                ),
                market_signals=item.get(
                    "market_signals", []
                ),
                confidence=item.get(
                    "confidence", "UNKNOWN"
                ),
            )
            for item in raw
        ]

    def _write(
        self,
        profiles: list[OpportunityProfile],
    ) -> None:
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = []

        for profile in profiles:
            item = asdict(profile)
            item["created_at"] = profile.created_at.isoformat()
            data.append(item)

        self.path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
