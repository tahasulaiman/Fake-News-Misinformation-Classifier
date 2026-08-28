class CredibilityScore:

    FAKE_THRESHOLD = 40
    SUSPICIOUS_THRESHOLD = 70

    def __init__(self, raw_score: float):
        self._raw_score = self._clamp(raw_score)

    @staticmethod
    def _clamp(score: float) -> float:
        return max(0.0, min(100.0, score))

    def get_score(self) -> float:
        return round(self._raw_score, 2)

    def get_label(self) -> str:
        score = self._raw_score
        if score < self.FAKE_THRESHOLD:
            return "Likely Fake"
        elif score < self.SUSPICIOUS_THRESHOLD:
            return "Suspicious"
        else:
            return "Likely Real"

    def __repr__(self):
        return f"CredibilityScore(score={self.get_score()}, label='{self.get_label()}')"


class WeightedScore(CredibilityScore):
    SOURCE_WEIGHT = 0.40
    SENTIMENT_WEIGHT = 0.35
    KEYWORD_WEIGHT = 0.25

    def __init__(self, source_score: float, sentiment_score: float, keyword_score: float):
        self._source_score = self._clamp(source_score)
        self._sentiment_score = self._clamp(sentiment_score)
        self._keyword_score = self._clamp(keyword_score)

        final_score = (
            self.SOURCE_WEIGHT * self._source_score
            + self.SENTIMENT_WEIGHT * self._sentiment_score
            + self.KEYWORD_WEIGHT * self._keyword_score
        )

        super().__init__(final_score)

    def get_breakdown(self) -> dict:
        return {
            "source_score": round(self._source_score, 2),
            "source_contribution": round(self.SOURCE_WEIGHT * self._source_score, 2),
            "sentiment_score": round(self._sentiment_score, 2),
            "sentiment_contribution": round(self.SENTIMENT_WEIGHT * self._sentiment_score, 2),
            "keyword_score": round(self._keyword_score, 2),
            "keyword_contribution": round(self.KEYWORD_WEIGHT * self._keyword_score, 2),
            "final_score": self.get_score(),
            "label": self.get_label(),
        }

    def __repr__(self):
        return (
            f"WeightedScore(final={self.get_score()}, label='{self.get_label()}', "
            f"source={self._source_score}, sentiment={self._sentiment_score}, "
            f"keyword={self._keyword_score})"
        )
