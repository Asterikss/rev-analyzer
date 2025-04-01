import streamlit as st
import plotly.express as px
from streamlit_lottie import st_lottie_spinner
import time

import core.utils as utils


utils.initialize("DataExplorer")

with st.sidebar:
  st.markdown(
    """
        <a href="https://github.com/Asterikss/rev-analyzer" title="Git"><img src="https://img.shields.io/badge/-black?logo=github&link=https%3A%2F%2Fgithub.com%2FAsterikss%2Frev-analyzer" style="height:28px; width:auto;"></a>
        """,
    unsafe_allow_html=True,
  )

font = "Georgia"

lottie_json = utils.load_lottiefile("assets/AnimationParrot.json")

c1, c2 = st.columns([24, 76])

with c1:
  st.write("\n")
  st.markdown("<h1 style='color: #ef6910;'>DataExplorer</h1>", unsafe_allow_html=True)
  st.write("\n")

st.header("Classification", anchor=False, divider="orange")

vc_classificatioin_dict = utils.get_vc_classificatioin_dict()

fig_vc_classification = px.bar(
  vc_classificatioin_dict,
  x="Class",
  y="Frequency",
  color="Frequency",
  template="plotly_dark",
)

fig_vc_classification.update_layout(
  plot_bgcolor="rgba(0,0,0,0)",
  paper_bgcolor="rgba(0,0,0,0)",
  xaxis=(dict(showgrid=False)),
  yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_vc_classification, use_container_width=True)

st.markdown(
  f"""
<div style="font-size: larger; font-weight: bold; font-family: {font};">
The above are the value counts for all the classes in the dataset used during
the fine-tuning of the classification model. Specifically I fine-tuned <a
href="https://huggingface.co/distilbert-base-cased">distilbert-base-cased</a>
on <a
href="https://huggingface.co/datasets/yyu/amazon-attrprompt">amazon-attrpromptx</a>
dataset for 3 epochs. Both can be found on Huggingface. The dataset has been used in this <a
href="https://arxiv.org/abs/2306.15895">paper</a>. Training code can be found
<a href="https://github.com/Asterikss/ai-notebooks/tree/master/rev_analyzer_build">here</a>.
 I uploaded this model to huggingface model hub. It's available at <a
href="https://huggingface.co/Asteriks/distilbert-cased-reviews-v1">Asteriks/distilbert-cased-reviews-v1</a>.
</div>
""",
  unsafe_allow_html=True,
)

bins_classification_dict = utils.get_len_bins_classification_dict()

fig_bins_classification = px.bar(
  bins_classification_dict,
  x="Bin",
  y="Frequency",
  title="Reviews by their length",
  color="Frequency",
  template="plotly_dark",
)

fig_bins_classification.update_layout(
  plot_bgcolor="rgba(0,0,0,0)",
  paper_bgcolor="rgba(0,0,0,0)",
  xaxis=(dict(showgrid=False)),
  yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_bins_classification, use_container_width=True)

st.header("Sentiment", anchor=False, divider="green")

st.markdown(
  f"""
<div style="font-size: larger; font-weight: bold; font-family: {font};">
For sentiment prediction, the models were trained on Amazon reviews dataset, accesible on both <a
href="https://huggingface.co/datasets/hugginglearners/amazon-reviews-sentiment-analysis">huggingface</a>
and <a href="https://www.kaggle.com/datasets/tarkkaanko/amazon">kaggle</a>.
Here is an overview.
</div>
""",
  unsafe_allow_html=True,
)

vc_sentiment_orig_dict = {
  "Rating": ["5.0", "4.0", "1.0", "3.0", "2.0"],
  "Frequency": [3921, 527, 244, 142, 80],
}

vc_sentiment_dict = {
  "Label": ["Negative", "Positive"],
  "Frequency": [324, 4448],
}

fig_sentiment_orig_dict = px.bar(
  vc_sentiment_orig_dict,
  x="Rating",
  y="Frequency",
  title="Original dataset",
  color="Rating",
  color_discrete_map={
    "5.0": "#ace600",
    "1.0": "#992600",
    "2.0": "#992600",
    "3.0": "#c2c2d6",
    "4.0": "#ace600",
  },
)

fig_sentiment_orig_dict.update_layout(
  plot_bgcolor="rgba(0,0,0,0)",
  paper_bgcolor="rgba(0,0,0,0)",
  xaxis=(dict(showgrid=False)),
  showlegend=False,
  yaxis=(dict(showgrid=False)),
)

fig_sentiment_dict = px.bar(
  vc_sentiment_dict,
  x="Label",
  y="Frequency",
  title="Dataset after transformation",
  color="Label",
  color_discrete_map={"Positive": "#ace600", "Negative": "#992600"},
)

fig_sentiment_dict.update_layout(
  plot_bgcolor="rgba(0,0,0,0)",
  paper_bgcolor="rgba(0,0,0,0)",
  xaxis=(dict(showgrid=False)),
  showlegend=False,
  yaxis=(dict(showgrid=False)),
)

fig_sent_1, fig_sent_2 = st.columns(2)

with fig_sent_1:
  st.plotly_chart(fig_sentiment_orig_dict, use_container_width=True)
with fig_sent_2:
  st.plotly_chart(fig_sentiment_dict, use_container_width=True)


st.markdown(
  f"""
<div style="font-size: larger; font-weight: bold; font-family: {font};">
Since the dataset is very imbalanced, oversampling (SMOTE) was integrated during the
training of each model except Naive Bayes. The preprocessing steps included: cleaning
the reviews, tokenization, removing stopwords and stemming. These steps utilized the nltk library.
Subsequently, the reviews where transformed into matrices using the Term Frequency-Inverse Document Frequency (TF-IDF)
vectorizer from the scikit-learn library and fed into the models. Training code can be found
<a href="https://github.com/Asterikss/ai-notebooks/tree/master/rev_analyzer_build">here</a>.
</div>
""",
  unsafe_allow_html=True,
)

# This is supposed to be at the end of the file
with c2:
  with st_lottie_spinner(lottie_json, height=90, width=90, speed=0.85, quality="low"):  # pyright: ignore[reportGeneralTypeIssues]
    time.sleep(3)
