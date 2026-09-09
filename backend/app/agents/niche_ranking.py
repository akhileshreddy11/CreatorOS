"""Deterministic niche ranking used by the business-intelligence pipeline."""


class NicheRanking:
    """Normalize and rank the researcher's niche candidates."""

    def rank(self, research: dict | None) -> dict:
        if not isinstance(research, dict):
            return {"ranked_niches": [], "best_niche": None, "status": "FAILED"}

        candidates = research.get("ranked_niches", [])
        if not isinstance(candidates, list):
            candidates = []

        normalized = [candidate for candidate in candidates if isinstance(candidate, dict)]
        normalized.sort(key=lambda item: self._score(item), reverse=True)

        for index, candidate in enumerate(normalized, start=1):
            candidate["rank"] = index

        best = research.get("best_niche")
        if not isinstance(best, dict) and normalized:
            best = normalized[0]
        elif isinstance(best, dict) and normalized:
            best = {**normalized[0], **best}

        return {
            "ranked_niches": normalized,
            "best_niche": best,
            "status": "READY" if best else "EMPTY",
        }

    @staticmethod
    def _score(candidate: dict) -> float:
        value = candidate.get("overall_score", 0)
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0
