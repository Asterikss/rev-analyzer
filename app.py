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

st.subheader("Enter a review to by analyzed below")
st.write("Or choose a predefined review:")

predefined_options = [
    "Red Hot Chili Peppers on vinyl has been a disappointing experience.. I had to return both “By The Way” and “Stadium Arcadium” because there were skips on almost all of it.. Kind of made it seem like the record label just went cheap, which is a disservice to anyone that actually listens to their vinyl...This “Greatest Hits” compilation did not have the same problems as the other two I bought. It sounded as it should have, and there were no skips.",
    "I love this shirt. It is really really soft"
]

button_0 = st.button(predefined_options[0])
button_1 = st.button(predefined_options[1])

user_input = st.text_input(
        "User input",
        placeholder="Enter a review to be analyzed",
        label_visibility="collapsed",
        # key="user_query",
    )

lbl_emoji_dict = {"music_album": "🎧",
                  "apparel": "👢"}


if user_input or button_0 or button_1:
    input_to_analyze = user_input if user_input else predefined_options[0] if button_0 else predefined_options[1]
    output = classifier([input_to_analyze])
    label = output[0]["label"] # type: ignore[reportOptionalSubscript]

    emoji = lbl_emoji_dict[label] # type: ignore[GeneralTypeIssues]
    with st.chat_message("user", avatar=emoji):
        st.write("Classified as: [  ", label, "  ] Confidence: ", output[0]["score"]) # type: ignore[reportOptionalSubscript]
