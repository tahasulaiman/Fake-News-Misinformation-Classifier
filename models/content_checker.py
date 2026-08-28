from abc import ABC, abstractmethod
from models.article import NewsArticle
from models.source import Source
from models.credibility_score import WeightedScore
from analysis.sentiment import SentimentAnalyzer
from analysis.scoring import KeywordScorer


class ContentChecker(ABC):
    def __init__(self):
        # Shared tools used by both subclasses
        self._sentiment_analyzer = SentimentAnalyzer()
        self._keyword_scorer = KeywordScorer()

    @abstractmethod
    def check(self, article: NewsArticle, source: Source) -> dict:
        pass

    def _build_result(self, article, source, checker_type: str) -> dict:
        sentiment_details = self._sentiment_analyzer.analyze(article.get_text())
        keyword_details = self._keyword_scorer.score(article.get_text())

        weighted_score = WeightedScore(
            source_score=source.get_reputation_score(),
            sentiment_score=sentiment_details["score"],
            keyword_score=keyword_details["score"],
        )

        return {
            "weighted_score": weighted_score,
            "sentiment_details": sentiment_details,
            "keyword_details": keyword_details,
            "checker_type": checker_type,
        }


class HeadlineChecker(ContentChecker):
    def check(self, article: NewsArticle, source: Source) -> dict:
        result = self._build_result(article, source, checker_type="Headline")

        # Headline-specific note for the GUI
        result["note"] = (
            "Analyzed as a HEADLINE: keyword/clickbait patterns are weighted "
            "heavily since headlines are designed to grab attention."
        )
        return result


class FullTextChecker(ContentChecker):
    def check(self, article: NewsArticle, source: Source) -> dict:
        result = self._build_result(article, source, checker_type="Full Article")

        result["note"] = (
            "Analyzed as a FULL ARTICLE: overall sentiment and subjectivity "
            "across the text carry more weight than isolated keywords."
        )
        return result


def get_checker_for_article(article: NewsArticle) -> ContentChecker:
    if article.is_headline():
        return HeadlineChecker()
    return FullTextChecker()
