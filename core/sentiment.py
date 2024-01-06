import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle


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


@st.cache_resource
def get_vectorizer():
    return pickle.load(open("models/tfidf_vectorizer.sav", "rb"))

@st.cache_resource
def get_lr_model():
    return pickle.load(open("models/logistic_regression_model.sav", "rb"))


def get_lr_prediction(input: str):
    return get_lr_model().predict(get_vectorizer().transform([input])).item()
