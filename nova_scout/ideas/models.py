from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Idea:
    name: str
    description: str = ""
    niche: str = ""
    target_market: str = ""
    currency: str = "USD"
    status: str = "NEW"
    id: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
