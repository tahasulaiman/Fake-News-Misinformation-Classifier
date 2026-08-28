from textblob import  TextBlob
from utils.exceptions import InvalidInputError , SentimentAnalysisError

class SentimentAnalyzer:
    def analyze(self,text : str) -> dict:
        if not text or not text.strip():
            raise InvalidInputError("Cannot analyze empty text.")
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except Exception as e:
            raise SentimentAnalysisError(f"TextBlob failed: {e}.")

        polarity_score = (1 - abs(polarity)) * 100
        subjectivity_penalty = subjectivity * 20

        score = max(0,min(100,polarity_score - subjectivity_penalty))

        flags = []
        if abs(polarity) > 0.5:
            if polarity > 0:
                tone = "very positive"
            else:
                tone = "very negative"
            flags.append(f"Highly emotional tone detected ({tone}).")
        else:
            flags.append("Tone is neutral.")

        if subjectivity > 0.5:
            flags.append("Text is highly subjective.")

        return{
            "polarity" : round(polarity , 2),
            "subjectivity" : round(subjectivity,2),
            "score" : round(score,2),
            "flags" : flags,
        }
