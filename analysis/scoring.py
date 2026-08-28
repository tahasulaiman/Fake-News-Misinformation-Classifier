import json
import re
from utils.exceptions import InvalidInputError


class KeywordScorer :
    def __init__(self, keywords_path = None):
        if keywords_path is None:
            keywords_path = "data/keywords.json"

        (
            self._clickbait_phrases,
            self._sensational_words,
            self._fake_claim_indicators
        ) = self._load_keywords(keywords_path)

    @staticmethod
    def _load_keywords(path:str):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return (
                [p.lower() for p in data.get("clickbait_phrases" , [])],
                [w.lower() for w in data.get("sensational_words" , [])],
                [g.lower() for g in data.get("fake_claim_indicators" , [])],
            )
        except (FileNotFoundError , json.JSONDecodeError):
            return [],[],[]

    def score(self, text : str):
        if not text or not text.strip():
            raise InvalidInputError("Cannot score empty text for keywords")
        score = 100.0
        flags = []
        lower_text = text.lower()

        for phrase in self._clickbait_phrases:
            if phrase in lower_text:
                score -= 15
                flags.append(f"Clickbait phrase detected : {phrase}")

        for word in self._sensational_words:
            if word in lower_text:
                score -= 8
                flags.append(f"Sensational word detected : {word}")

        for indicators in self._fake_claim_indicators:
            if indicators in lower_text:
                score -= 5
                flags.append(f"Fake indicator detected : {indicators}")

        exclamations = text.count("!")
        if exclamations >= 2:
            minus = min(exclamations * 5 , 20)
            score -= minus
            flags.append(f"Excessive exclamation marks ({exclamations} found) ")

        caps = re.findall(r"\b[A-Z]{4,}\b" , text)
        if caps:
            minus = min(len(caps)* 5 , 10)
            score -= minus
            flags.append(f"ALL CAPS words detected: {', '.join(set(caps))}")

        score = max(0 ,min(100 , score))

        if not flags:
            flags.append("No clickbait,sensational or fake indicators detected.")

        return {
            "score" : round(score, 2),
            "flags" : flags}
