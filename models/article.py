from utils.exceptions import InvalidInputError

class NewsArticle:
    def __init__(self, text , source_name):
        if not text or not text.strip():
            raise InvalidInputError("News text cannot be empty.")

        self._text = text.strip()
        self._source_name = source_name.strip() if source_name else "Unknown"
        self._word_count = len(self._text.split())

    def get_text(self) -> str:
        return self._text

    def get_source_name(self) -> str:
        return  self._source_name

    def get_word_count(self) -> int:
        return self._word_count

    def is_headline(self,word_threshold : int = 20) -> bool:
        return  self._word_count <= word_threshold

    def __repr__(self):
        preview = self._text[:40] + ("..." if len(self._text) > 40 else "")
        return f"NewsArticle(source = '{self._source_name}' , text = '{preview}')"