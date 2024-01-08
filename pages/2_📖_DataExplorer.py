import streamlit as st
import plotly.express as px
from core.utils import get_vc_classificatioin_dict

st.set_page_config(
    page_title="DataExplorer",
    page_icon="📖",
    layout="wide",
)

st.title("DataExplorer", anchor=False)
st.header("Classification", anchor=False, divider="red")

vc_classificatioin_dict = get_vc_classificatioin_dict()

fig_vc_classification = px.bar(
    vc_classificatioin_dict,
    x="Class",
    y="Frequency",
    # title="Value Counts",
    color="Frequency",
    # color_discrete_sequence==
    template="plotly_white",
)

fig_vc_classification.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_vc_classification, use_container_width=True)
