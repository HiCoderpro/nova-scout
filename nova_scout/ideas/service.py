from .models import Idea
from .repository import IdeaRepository


class IdeaService:
    def __init__(self, repository: IdeaRepository):
        self.repository = repository

    def create(
        self,
        name: str,
        description: str = "",
        niche: str = "",
        target_market: str = "",
        currency: str = "USD",
    ) -> Idea:
        name = name.strip()

        if not name:
            raise ValueError("Idea name cannot be empty.")

        idea = Idea(
            name=name,
            description=description.strip(),
            niche=niche.strip(),
            target_market=target_market.strip(),
            currency=currency.upper(),
        )

        return self.repository.save(idea)

    def get(self, idea_id: str) -> Idea | None:
        return self.repository.get(idea_id)

    def list(self) -> list[Idea]:
        return self.repository.list()
