import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle
from typing import Dict, Any

from core.utils import Model


@st.cache_data
def get_sid() -> Any:
    return SentimentIntensityAnalyzer()


def get_naive_sentiment(input: str) -> Dict:
    return get_sid().polarity_scores(input)


@st.cache_resource
def get_vectorizer() -> Any:
    return pickle.load(open("models/tfidf_vectorizer.sav", "rb"))


@st.cache_resource
def get_lr_model() -> Any:
    return pickle.load(open("models/logistic_regression_model.sav", "rb"))


@st.cache_resource
def get_nb_model() -> Any:
    return pickle.load(open("models/naive_bayes_model.sav", "rb"))


@st.cache_resource
def get_svm_model() -> Any:
    return pickle.load(open("models/svm_model.sav", "rb"))


def get_sentiment_prediction(input: str, model: Model) -> float:
    if model == Model.LR:
        return get_lr_model().predict(get_vectorizer().transform([input])).item()
    if model == Model.NB:
        return get_nb_model().predict(get_vectorizer().transform([input])).item()

    return get_svm_model().predict(get_vectorizer().transform([input])).item()
