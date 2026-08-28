# Fake News & Misinformation Classifier Tool
A modular Python-based application that analyzes news headlines and articles to determine their credibility using source reputation, sentiment analysis, and clickbait detection.

---

## Project Overview

This system is designed to simulate a real-world fake news detection workflow. It demonstrates NLP integration, weighted scoring algorithms, and modular OOP application design.

The project focuses on:
- Structured GUI development using Streamlit
- SQLite database management for source reputation and history
- Natural Language Processing using TextBlob
- Object-Oriented Programming (Abstraction, Inheritance, Polymorphism, Encapsulation)
- Modular file organization across separate packages

---

## Key Features

- Credibility scoring using a weighted formula: `0.40 × source + 0.35 × sentiment + 0.25 × keywords`
- Source reputation database with 18+ pre-seeded news outlets (Dawn, BBC, Reuters, etc.)
- Sentiment analysis using TextBlob — detects emotional/biased tone
- Clickbait detection via regex (ALL CAPS, `!!!`, sensational phrases)
- Persistent history log of all past checks stored in SQLite
- Custom exception handling — no raw tracebacks ever shown in GUI
- Clean color-coded verdict: 🟢 Likely Real · 🟡 Suspicious · 🔴 Likely Fake

---

## Tech Stack

- Python
- Streamlit (GUI)
- SQLite (Database)
- TextBlob (Sentiment Analysis)
- Pandas (Data Display)
- Regular Expressions (Clickbait Detection)

---

## Project Structure

```
fake_news_classifier/
│
├── main.py
├── requirements.txt
│
├── models/
│   ├── article.py
│   ├── source.py
│   ├── content_checker.py
│   └── credibility_score.py
│
├── analysis/
│   ├── sentiment.py
│   └── scoring.py
│
├── database/
│   ├── db_manager.py
│   └── schema.sql
│
├── data/
│   └── keywords.json
│
└── utils/
    └── exceptions.py
```

- `main.py` → Streamlit entry point and all 3 GUI screens
- `models/content_checker.py` → Abstract class + HeadlineChecker + FullTextChecker
- `models/credibility_score.py` → CredibilityScore base + WeightedScore (formula)
- `models/article.py` → NewsArticle class with input validation
- `models/source.py` → Source class with encapsulated reputation score
- `analysis/sentiment.py` → TextBlob wrapper converting tone to 0–100 score
- `analysis/scoring.py` → Keyword/clickbait scorer using regex + JSON lists
- `database/db_manager.py` → Centralized SQLite CRUD operations
- `database/schema.sql` → Table definitions + 18 seeded news sources
- `data/keywords.json` → Clickbait phrase and sensational word lists
- `utils/exceptions.py` → 4 custom exception classes

---

## Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/M3M397/fake-news-classifier.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download TextBlob language data *(run once)*:
```bash
python -m textblob.download_corpora
```

4. Run the application:
```bash
streamlit run main.py
```

Open your browser at **http://localhost:8501**

---

## Purpose of This Project

This project demonstrates my ability to:
- Design modular Python applications using OOP principles
- Integrate relational databases with application logic
- Apply NLP techniques for real-world text classification
- Build functional, modern GUI applications
- Handle errors gracefully using custom exception hierarchies

---
