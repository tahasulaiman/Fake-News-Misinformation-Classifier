class Source:
    def __init__(self, name: str, reputation_score: float, category: str = "General"):
        self._name = name
        self._reputation_score = self._validate_score(reputation_score)
        self._category = category

    @staticmethod
    def _validate_score(score: float) -> float:
        return max(0, min(100, score))

    def get_name(self) -> str:
        return self._name

    def get_reputation_score(self) -> float:
        return self._reputation_score

    def set_reputation_score(self, new_score: float):
        self._reputation_score = self._validate_score(new_score)

    def get_category(self) -> str:
        return self._category

    def get_trust_level(self) -> str:
        score = self._reputation_score
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    def __repr__(self):
        return f"Source(name='{self._name}', score={self._reputation_score}, trust='{self.get_trust_level()}')"
