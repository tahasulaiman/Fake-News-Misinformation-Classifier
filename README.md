# Fake News & Misinformation Classifier

A Python-based application developed as a **4-member Object-Oriented Programming group project** to analyze news headlines and articles and provide a credibility assessment.

The application combines source reputation, sentiment analysis, keyword/clickbait detection, and weighted scoring to classify news content as **Likely Real, Suspicious, or Likely Fake**.

## 🚀 Features

* News headline and article credibility analysis
* Source reputation scoring
* Sentiment analysis using TextBlob
* Clickbait and sensational keyword detection
* Weighted credibility scoring
* SQLite database for source information and checking history
* Streamlit-based user interface
* Custom exception handling
* Modular Object-Oriented Programming structure

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **SQLite**
* **TextBlob**
* **Pandas**
* **Regular Expressions (Regex)**

## 🧠 OOP Concepts

The project demonstrates several Object-Oriented Programming concepts:

* Abstraction
* Inheritance
* Polymorphism
* Encapsulation

## 👨‍💻 My Contribution

As one of the four members of the team, I was responsible for the **database component** of the project.

My work included:

* Designing the SQLite database structure
* Creating the `sources` and `history` tables
* Adding initial news-source data
* Implementing database connection and initialization
* Developing CRUD operations for news sources
* Implementing functionality to store and retrieve checking history
* Handling database-related errors through custom exceptions

### Database Structure

The database consists primarily of two tables:

**`sources`**

* Stores news-source names
* Reputation scores
* Source categories

**`history`**

* Stores analyzed content
* Source information
* Checker type
* Final credibility score
* Verdict
* Individual scoring components
* Timestamp

## 📁 Project Structure

```text
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
│   ├── schema.sql
│   └── fake_news.db
│
├── data/
│   └── keywords.json
│
└── utils/
    └── exceptions.py
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/M3M397/fake-news-classifier.git
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Download TextBlob language data:

```bash
python -m textblob.download_corpora
```

## ▶️ Running the Application

Run the Streamlit application:

```bash
streamlit run main.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🎯 Project Purpose

This project was developed to gain practical experience with:

* Object-Oriented Programming
* Database integration
* Natural Language Processing
* Modular Python application development
* Team-based software development
* Building a functional Streamlit application

## 👥 Team Project

This project was developed collaboratively by a **team of four students** as part of our Object-Oriented Programming coursework.
