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

@st.cache_resource
def get_classifier():
    return pipeline("text-classification", model="Asteriks/distilbert-cased-reviews-v1")

classifier = get_classifier()


user_input = st.text_area("Enter a review to be analyzed")

predefined_options = [
    "Red Hot Chili Peppers on vinyl has been a disappointing experience.. I had to return both “By The Way” and “Stadium Arcadium” because there were skips on almost all of it.. Kind of made it seem like the record label just went cheap, which is a disservice to anyone that actually listens to their vinyl...This “Greatest Hits” compilation did not have the same problems as the other two I bought. It sounded as it should have, and there were no skips.",
    "I love this shirt. It is really really soft"
]

selected_option = st.selectbox("Or choose a predefined review:", predefined_options)

analyze_button = st.button("Analyze")

input_to_analyze = selected_option if selected_option else user_input

if input_to_analyze and analyze_button:
    output = classifier([input_to_analyze])
    label = output[0]["label"] # type: ignore[reportOptionalSubscript]
    st.write("Classified as: [  ", label, "  ] Confidence: ", output[0]["score"]) # type: ignore[reportOptionalSubscript]
