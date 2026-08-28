import sqlite3
import os

from models.source import Source
from utils.exceptions import DatabaseConnectionError, SourceNotFoundError


class DatabaseManager:
    def __init__(self, db_path: str = None, schema_path: str = None):
        if db_path is None:
            db_path = "database/fake_news.db"
        if schema_path is None:
            schema_path = "database/schema.sql"

        self._db_path = db_path
        self._schema_path = schema_path
        self._initialize_db()

    def _get_connection(self):
        try:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Failed to connect to database: {e}")

    def _initialize_db(self):
        try:
            with open(self._schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()

            conn = self._get_connection()
            conn.executescript(schema_sql)
            conn.commit()
            conn.close()
        except (sqlite3.Error, FileNotFoundError) as e:
            raise DatabaseConnectionError(f"Failed to initialize database: {e}")

    # ---------- SOURCE METHODS ----------

    def get_source(self, name: str) -> Source:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM sources WHERE LOWER(name) = LOWER(?)", (name,)
        )
        row = cursor.fetchone()

        if row is None:
            # Fall back to the 'Unknown' source
            cursor.execute("SELECT * FROM sources WHERE name = 'Unknown'")
            row = cursor.fetchone()
            if row is None:
                conn.close()
                raise SourceNotFoundError(name)

        conn.close()
        return Source(row["name"], row["reputation_score"], row["category"])

    def get_all_sources(self) -> list:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sources ORDER BY reputation_score DESC")
        rows = cursor.fetchall()
        conn.close()

        return [Source(r["name"], r["reputation_score"], r["category"]) for r in rows]

    def add_source(self, source: Source):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO sources (name, reputation_score, category)
               VALUES (?, ?, ?)
               ON CONFLICT(name) DO UPDATE SET
                   reputation_score = excluded.reputation_score,
                   category = excluded.category""",
            (source.get_name(), source.get_reputation_score(), source.get_category()),
        )
        conn.commit()
        conn.close()

    # ---------- HISTORY METHODS ----------

    def log_check(self, input_text: str, source_name: str, checker_type: str,
                   weighted_score, sentiment_score: float, keyword_score: float):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO history
               (input_text, source_name, checker_type, final_score, label,
                source_score, sentiment_score, keyword_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                input_text,
                source_name,
                checker_type,
                weighted_score.get_score(),
                weighted_score.get_label(),
                weighted_score.get_breakdown()["source_score"],
                sentiment_score,
                keyword_score,
            ),
        )
        conn.commit()
        conn.close()

    def get_history(self, limit: int = 50) -> list:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM history ORDER BY timestamp DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
