import streamlit as st
from transformers import pipeline

from core.named_entity_recognition import compute_ner

st.set_page_config(
    page_title="ReviewAnalyzer",
    page_icon="🔬",
    layout="wide"
)

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
                  "apparel": "👢",
                  "magazines": "📖",
                  "camera_photo": "📽️",
                  "health_and_personal_care": "💪",
                  "electronics": "💻",
                  "outdoor_living": "🌄",
                  "video": "📽️",
                  "toys_games": "🕹️",
                  "sports_outdoors": "🚴",
                  "books": "📚",
                  "software": "💿",
                  "baby": "🍼",
                  "office_products": "🗃️",
                  "musical_and_instruments": "🎷",
                  "beauty": "🛀",
                  "jewelry_and_watches": "💎",
                  "kitchen": "🔪",
                  "cell_phones_service": "📱",
                  "computer_video_games": "🎮",
                  "grocery_and_gourmet_food": "🥕",
                  "tools_hardware": "🛠️",
                  "automotive": "🚗",
}


if user_input or button_0 or button_1:
    input_to_analyze = predefined_options[0] if button_0 else predefined_options[1] if button_1 else user_input

    if len(input_to_analyze) < 20:
        st.warning("Remeber that the model needs to have some context. It might struggle if the input is to short")

    output = classifier([input_to_analyze])
    label = output[0]["label"] # type: ignore[reportOptionalSubscript]

    emoji = lbl_emoji_dict[label] # type: ignore[GeneralTypeIssues]

    works_of_art, people = compute_ner(input_to_analyze)

    with st.chat_message("user", avatar=emoji):
        st.write("Classified as: [  ", label, "  ] Confidence: ", output[0]["score"]) # type: ignore[reportOptionalSubscript]

        if works_of_art:
            st.write("*", "Works of art found:")
            for woa in works_of_art:
                st.button(woa)

        if people:
            st.write("*", "People mentioned:")
            for woa in people:
                st.button(woa)

