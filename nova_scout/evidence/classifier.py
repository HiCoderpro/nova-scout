from __future__ import annotations

from nova_scout.evidence.models import Evidence


class EvidenceClassifier:
    """Classify evidence using source type and content."""

    SUPPORTED_TYPES = {
        "demand",
        "competition",
        "pricing",
        "market",
    }

    def classify(self, evidence: Evidence) -> Evidence:
        source_type = evidence.source_type.strip().lower()

        if source_type in self.SUPPORTED_TYPES:
            classifications = [source_type]
        else:
            classifications = self._classify_content(evidence)

        evidence.metadata["classification"] = (
            classifications[0] if classifications else "unknown"
        )
        evidence.metadata["classifications"] = classifications

        return evidence

    def _classify_content(self, evidence: Evidence) -> list[str]:
        text = f"{evidence.title} {evidence.content}".lower()

        classifications = []

        demand_keywords = (
            "search",
            "searches",
            "searching",
            "users",
            "demand",
            "customers",
            "looking for",
        )

        competition_keywords = (
            "competitor",
            "competitors",
            "competition",
            "competitive",
            "alternative",
            "alternatives",
        )

        pricing_keywords = (
            "price",
            "pricing",
            "priced",
            "charge",
            "charges",
            "cost",
            "costs",
            "per month",
            "per year",
            "$",
        )

        market_keywords = (
            "market",
            "global",
            "industry",
            "countries",
            "country",
            "sector",
            "market size",
        )

        if any(keyword in text for keyword in demand_keywords):
            classifications.append("demand")

        if any(keyword in text for keyword in competition_keywords):
            classifications.append("competition")

        if any(keyword in text for keyword in pricing_keywords):
            classifications.append("pricing")

        if any(keyword in text for keyword in market_keywords):
            classifications.append("market")

        return classifications or ["unknown"]
