import streamlit as st
import pandas as pd
from models.article import NewsArticle
from models.content_checker import get_checker_for_article
from database.db_manager import DatabaseManager
from utils.exceptions import (
    InvalidInputError,
    SourceNotFoundError,
    DatabaseConnectionError,
    SentimentAnalysisError,
)

st.set_page_config(
    page_title="Fake News & Misinformation Classifier Tool",
    layout="centered",
    page_icon="🔎"
)

@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

st.sidebar.title("Fake News & Misinformation Classifier Tool")
select = st.sidebar.radio(
    "Navigation",
    ["Detector", "Sources", "History"]
)

#----------Page 1 ------------
if select == "Detector":
    st.title("Check a Headline or Article.")
    st.write("Paste a news headline or article below, and get a credibility score.")

    text_input = st.text_area("News Headline or Article text", height=200)

    try:
        all_sources = db.get_all_sources()
        source_names = [s.get_name() for s in all_sources]

        if not source_names:
            source_names = ["Unknown"]

    except DatabaseConnectionError as e:
        st.error(f"Database error: {e}")
        source_names = ["Unknown"]

    selected_source = st.selectbox(
        "Source",
        source_names,
        index=source_names.index("Unknown") if "Unknown" in source_names else 0
    )

    if st.button("Check Credibility", type="primary"):
        if not text_input or not text_input.strip():
            st.error("News text cannot be empty.")
        else:
            try:
                article = NewsArticle(text_input, source_name=selected_source)
                source = db.get_source(selected_source)
                checker = get_checker_for_article(article)
                result = checker.check(article, source)

                weighted_score = result["weighted_score"]
                breakdown = weighted_score.get_breakdown()

                db.log_check(
                    input_text=article.get_text(),
                    source_name=source.get_name(),
                    checker_type=result["checker_type"],
                    weighted_score=weighted_score,
                    sentiment_score=result["sentiment_details"]["score"],
                    keyword_score=result["keyword_details"]["score"],
                )

                st.markdown("---")
                label = weighted_score.get_label()
                score = weighted_score.get_score()

                if label == "Likely Real":
                    st.success(f"**{label}** —  Credibility Score: {score}/100")
                elif label == "Suspicious":
                    st.warning(f"**{label}** —  Credibility Score: {score}/100")
                else:
                    st.error(f"**{label}** —  Credibility Score: {score}/100")

                st.progress(int(score))

                st.caption(
                    f"Analyzed as: **{result['checker_type']}** "
                    f"({article.get_word_count()} words)"
                )
                st.info(result["note"])

                with st.expander("Why this score? (breakdown)", expanded=True):
                    st.markdown(f"""
| Factor | Sub-score (0-100) | Weight | Contribution |
|---|---|---|---|
| Source reputation ({source.get_name()}) | {breakdown['source_score']} | 40% | {breakdown['source_contribution']} |
| Sentiment / tone | {breakdown['sentiment_score']} | 35% | {breakdown['sentiment_contribution']} |
| Keyword / clickbait | {breakdown['keyword_score']} | 25% | {breakdown['keyword_contribution']} |
| **Final Score** | | | **{breakdown['final_score']}** |
""")

                    st.markdown("**Sentiment notes:**")
                    for flag in result["sentiment_details"]["flags"]:
                        st.write(f"- {flag}")

                    st.markdown("**Keyword notes:**")
                    for flag in result["keyword_details"]["flags"]:
                        st.write(f"- {flag}")

            except SourceNotFoundError:
                st.warning(
                    f"Source '{selected_source}' is not in the database yet. Please add it in the 'Sources' tab to get an accurate score!")
            except InvalidInputError as e:
                st.warning(f"{e}")
            except SentimentAnalysisError as e:
                st.error(f"{e}")
            except DatabaseConnectionError as e:
                st.error(f"Database error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

#----------Page 2 ------------
elif select == "Sources":
    st.title("Sources")
    st.write("Browse the reputation scores used to evaluate news sources.")

    try:
        sources = db.get_all_sources()
        data = [
            {
                "Source": s.get_name(),
                "Reputation Score": s.get_reputation_score(),
                "Trust Level": s.get_trust_level(),
                "Category": s.get_category(),
            }
            for s in sources if s.get_name().strip()
        ]
        df = pd.DataFrame(data)

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("Add a new source")

        with st.form("add_source_form"):
            new_name = st.text_input("Source name")
            new_score = st.slider("Reputation score", 0, 100, 50)
            new_category = st.text_input("Category", value="General")
            submitted = st.form_submit_button("Add Source")

            if submitted:
                if not new_name.strip():
                    st.error("⚠️ Source name cannot be blank!")
                else:
                    try:
                        from models.source import Source

                        new_source = Source(new_name, new_score, new_category)
                        db.add_source(new_source)
                        st.success(f"Added/updated source: {new_name}")
                        st.rerun()
                    except InvalidInputError as e:
                        st.warning(f"{e}")
                    except Exception as e:
                        st.error(f"Error adding source: {e}")

    except DatabaseConnectionError as e:
        st.error(f"Database error: {e}")
#----------Page 3 ------------
elif select == "History":
    st.title("History")
    st.write("Recent credibility checks performed.")

    try:
        history = db.get_history(limit=50)

        if not history:
            st.info("No checks have been performed yet. Go to 'Detector' to check something!")
        else:
            df = pd.DataFrame(history)

            display_cols = [
                "timestamp", "input_text", "source_name", "checker_type",
                "final_score", "label",
            ]
            df = df[display_cols]
            df = df.rename(columns={
                "timestamp": "Time",
                "input_text": "Text",
                "source_name": "Source",
                "checker_type": "Checker",
                "final_score": "Score",
                "label": "Label",
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

    except DatabaseConnectionError as e:
        st.error(f"Database error: {e}")
