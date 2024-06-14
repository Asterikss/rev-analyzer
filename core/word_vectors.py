import streamlit as st
import re
import plotly.express as px
from gensim.models import KeyedVectors
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.decomposition import PCA
from typing import Dict, List, Any


@st.cache_data
def get_stop_wrods() -> List[str]:
    return stopwords.words("english")


def get_processed_tokens(text, key_to_index) -> List[str]:
    text = re.sub(r"[^a-zA-Z\s]", "", text).lower()

    lemmer = WordNetLemmatizer()

    cleaned_tokens = [
        lemmer.lemmatize(token)
        for token in word_tokenize(text)
        if token not in get_stop_wrods()
    ]

    return [token for token in cleaned_tokens if token in key_to_index.keys()]


@st.cache_resource
def load_glove_vectors() -> Any:
    return KeyedVectors.load("models/glove-wiki-gigaword-50.model")


# UnhashableParamError: Cannot hash argument 'glove_vectors' (of type gensim.models.keyedvectors.KeyedVectors) in 'get_key_to_index'.
# To address this, you can tell Streamlit not to hash this argument by adding a leading underscore to the argument's name in the function signature:
@st.cache_data
def get_key_to_index(_glove_vectors) -> Dict:
    return _glove_vectors.key_to_index


def get_scatterplot(glove_vectors, tokens, normalize_wv: bool=True):
    word_vectors = [glove_vectors.get_vector(t, norm=normalize_wv) for t in tokens]

    twodim = PCA(n_components=2).fit_transform(word_vectors)

    word_vectors_2d_dict = {
        "word": tokens,
        "x": [coord[0] for coord in twodim.tolist()],
        "y": [coord[1] for coord in twodim.tolist()],
        "color": [coord[0] + coord[1] for coord in twodim.tolist()],
    }

    fig = px.scatter(
        word_vectors_2d_dict,
        x="x",
        y="y",
        text="word",
        color="color",
        color_continuous_scale="mygbm",
    )

    fig.update_traces(textposition="top center")

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False, showticklabels=False, visible=False)),
        yaxis=(dict(showgrid=False, showticklabels=False, visible=False)),
    )

    return fig


def plot_words(input_to_analyze: str, normalize_wv: bool=True) -> None:
    glove_vectors = load_glove_vectors()
    key_to_index = get_key_to_index(glove_vectors)
    processed_tokens = get_processed_tokens(input_to_analyze, key_to_index)
    plot = get_scatterplot(glove_vectors, processed_tokens, normalize_wv)
    st.plotly_chart(plot, use_container_width=True)
