
class InvalidInputError(Exception):
    def __init__(self, message="Input text cannot be empty or invalid."):
        self.message = message
        super().__init__(self.message)

class SourceNotFoundError(Exception):
    def __init__(self, source_name="Unknown"):
        self.source_name = source_name
        self.message = f"Source '{source_name}' not found in database."
        super().__init__(self.message)

class DatabaseConnectionError(Exception):
    def __init__(self, message="Could not connect to the database."):
        self.message = message
        super().__init__(self.message)

class SentimentAnalysisError(Exception):
    def __init__(self, message="Sentiment analysis failed for the given text."):
        self.message = message
        super().__init__(self.message)
