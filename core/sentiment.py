import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


@st.cache_data
def get_sid():
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon")
    return SentimentIntensityAnalyzer()


def get_naive_sentiment(input: str):
    sid = get_sid()
    return sid.polarity_scores(input)
