import streamlit as st
from transformers import pipeline

page =  """
<style>
body {
    background-color: #1E1E1E;
    color: #FFFFFF;
}
</style>
"""

st.markdown(page, unsafe_allow_html=True)
st.title("ReviewAnalyzer")

@st.cache(allow_output_mutation=True)
def get_classifier():
    return pipeline("text-classification", model="Asteriks/distilbert-cased-reviews-v1")

classifier = get_classifier()


user_input = st.text_area("Enter a review to be analyzed")
analyze_button = st.button("Analyze")


if user_input and analyze_button:
    st.write("Classified as: ", classifier([user_input])) 
