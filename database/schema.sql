-- SQLite schema for Fake News & Misinformation Classifier
-- Two tables: sources (reputation database) and history (past checks)

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    reputation_score REAL NOT NULL CHECK (reputation_score >= 0 AND reputation_score <= 100),
    category TEXT DEFAULT 'General'
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text TEXT NOT NULL,
    source_name TEXT NOT NULL,
    checker_type TEXT NOT NULL,
    final_score REAL NOT NULL,
    label TEXT NOT NULL,
    source_score REAL,
    sentiment_score REAL,
    keyword_score REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Seed data: ~18 sources (mix of reputable, average, and known-unreliable)
INSERT OR IGNORE INTO sources (name, reputation_score, category) VALUES
    ('Dawn', 88, 'National News'),
    ('BBC', 92, 'International News'),
    ('Reuters', 93, 'International News'),
    ('Al Jazeera', 85, 'International News'),
    ('The Express Tribune', 78, 'National News'),
    ('Geo News', 70, 'National News'),
    ('ARY News', 65, 'National News'),
    ('CNN', 80, 'International News'),
    ('The News International', 75, 'National News'),
    ('Samaa TV', 60, 'National News'),
    ('Associated Press', 91, 'International News'),
    ('Al Bawaba', 45, 'Regional News'),
    ('Unknown', 50, 'Unverified'),
    ('Daily Mail', 40, 'Tabloid'),
    ('The Onion', 25, 'Satire'),
    ('World Truth TV', 15, 'Known Unreliable'),
    ('Before It''s News', 10, 'Known Unreliable'),
    ('NewsPunch', 12, 'Known Unreliable');
