import streamlit as st

import core.utils
from core.models import query_classifier
from core.named_entity_recognition import compute_ner

st.set_page_config(page_title="ReviewAnalyzer", page_icon="🔬", layout="wide")

st.title("ReviewAnalyzer")

with st.sidebar:
    extract_entities = st.toggle("Extract entities", value=True)
    predict_tone = st.toggle("Predict tone", value=True)
    num_probs = st.slider("How many probabilities to display?", 1, 4, 1)


st.subheader("Enter a review to by analyzed below")
st.write("Or choose a predefined review:")


predefined_options = [
    "Red Hot Chili Peppers on vinyl has been a disappointing experience.. I had to return both “By The Way” and “Stadium Arcadium” because there were skips on almost all of it.. Kind of made it seem like the record label just went cheap, which is a disservice to anyone that actually listens to their vinyl...This “Greatest Hits” compilation did not have the same problems as the other two I bought. It sounded as it should have, and there were no skips.",
    "I've read a number of Stephen King's works over the past 15 years. King has always genuinely impressed me with his incredible eye for detail, his sense of place, and his ability to steadily pay out the rope line of a story's plot. Additionally, of course, he's the Jedi Master of creepiness. Although I was familiar with the premise of “The Stand”, it still scared me a lot",
]


def clear_user_input():
    st.session_state.user_input = ""


button_0 = st.button(predefined_options[0], on_click=clear_user_input)
button_1 = st.button(predefined_options[1], on_click=clear_user_input)

lbl_emoji_dict = core.utils.get_lbl_emoji_dict()


st.text_input(
    "User input",
    placeholder="Enter a review to be analyzed",
    label_visibility="collapsed",
    key="user_input",
)


def update_state(input):
    st.session_state.selected_text = input


if "selected_text" not in st.session_state:
    st.session_state.selected_text = ""

if st.session_state.user_input or button_0 or button_1:
    input_to_analyze = (
        predefined_options[0]
        if button_0
        else predefined_options[1]
        if button_1
        else st.session_state.user_input
    )

    if len(input_to_analyze) < 25:
        st.warning(
            "Remeber that the model needs to have some context. It might struggle if the input is to short"
        )

    output = query_classifier(input_to_analyze)
    label = output[1][0]

    emoji = lbl_emoji_dict[label]

    works_of_art, people = compute_ner(input_to_analyze)

    with st.chat_message("user", avatar=emoji):
        st.write("Classified as: [  ", label, "  ] Confidence: ", output[0][0])
        for i in range(1, num_probs):
            st.markdown(f'<span style="color:grey">{output[1][i]} - {output[0][i]}</span>', unsafe_allow_html=True)

        if extract_entities:
            if works_of_art:
                st.write("*", "Works of art found:")
                for text in works_of_art:
                    st.button(text, on_click=update_state, args=(text,))

            if people:
                st.write("*", "People mentioned:")
                for text in people:
                    st.button(text, on_click=update_state, args=(text,))

            st.success(
                "You can click any of the phrases to search for them on the Wiki"
            )


if st.session_state.selected_text:
    st.subheader("Phrase choosen: " + st.session_state.selected_text)
    search_wiki = st.button("Search Wiki")

    if search_wiki:
        with st.spinner("4Wait for it..."):
            st.write(st.session_state.selected_text)
            st.success("Searching ...")
