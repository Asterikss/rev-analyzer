import streamlit as st
import plotly.express as px
import core.utils as utils

utils.initialize("DataExplorer")

st.title(":orange[DataExplorer]", anchor=False)
st.header("Classification", anchor=False, divider="rainbow")

vc_classificatioin_dict = utils.get_vc_classificatioin_dict()

fig_vc_classification = px.bar(
    vc_classificatioin_dict,
    x="Class",
    y="Frequency",
    color="Frequency",
    # color_discrete_sequence==
    template="plotly_white",
)

fig_vc_classification.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_vc_classification, use_container_width=True)

st.markdown( f"""
<h5>
The above are the value counts for all the classes in the dataset used during
the fine-tuing of the classification model. Specifically I fine-tuined <a
href="https://huggingface.co/distilbert-base-cased">distilbert-base-cased</a>
on <a
href="https://huggingface.co/datasets/yyu/amazon-attrprompt">amazon-attrpromptx</a>
dataset. Both can be found on Huggingface. The dataset has been used in this <a
href="https://arxiv.org/abs/2306.15895">paper</a> Training code can be found at
todo. I uploaded this model to huggingface model hub. It is available at <a
href="https://huggingface.co/Asteriks/distilbert-cased-reviews-v1">Asteriks/distilbert-cased-reviews-v1</a>.
<h5>
""", unsafe_allow_html=True)

bins_classification_dict = utils.get_len_bins_classification_dict()

fig_bins_classification = px.bar(
    bins_classification_dict,
    x="Bin",
    y="Frequency",
    title="Reviews by their length",
    color="Frequency",
    template="plotly_white",
)

fig_bins_classification.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_bins_classification, use_container_width=True)

st.header("Sentiment", anchor=False, divider="rainbow")
