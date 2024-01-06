import streamlit as st

import core.utils
from core.models import query_classifier
from core.named_entity_recognition import compute_ner
from core.wiki_service import get_wikipedia_summary
from core.sentiment import get_naive_sentiment

core.utils.initialize()

st.title(":blue[ReviewAnalyzer]", anchor=False)

with st.sidebar:
    predict_sentiment = st.toggle("Predict sentiment", value=True)
    extract_entities = st.toggle("Extract entities", value=True)
    num_probs = st.slider("How many probabilities to display?", 1, 4, 1)
    with st.expander("Additional settings"):
        if predict_sentiment:
            values = st.slider(
                "Select a range of values for sentiment analysis score",
                -0.9,
                0.9,
                (-0.2, 0.2),
                step=0.1,
            )


st.subheader("Enter a review to by analyzed below", anchor=False)
st.write("Or choose a predefined review:")

predefined_options = core.utils.get_predefined_options()

tabs = st.tabs(["Example " + str(i + 1) for i in range(len(predefined_options))])
for i, tab in enumerate(tabs):
    with tab:
        st.button(
            predefined_options[i],
            key=i,
            on_click=core.utils.clear_memory,
            args=("all",),
        )

st.text_area(  # used to be text_input
    "User input",
    placeholder="Enter a review to be analyzed",
    label_visibility="collapsed",
    key="user_input",
    on_change=core.utils.clear_memory,
    args=("selected_text",),
)

pressed_button_index = next(
    (i for i in range(len(predefined_options)) if st.session_state[i]), None
)

if st.session_state.user_input or pressed_button_index is not None:
    input_to_analyze = (
        predefined_options[pressed_button_index]
        if pressed_button_index is not None
        else st.session_state.user_input
    )

    if len(input_to_analyze) < 25:
        st.warning(
            "Remeber that the model needs to have some context. It might struggle\
            if the input is to short or vauge"
        )

    output = query_classifier(input_to_analyze)
    label = output[1][0]

    emoji = core.utils.get_lbl_emoji_dict()[label]

    with st.chat_message("user", avatar=emoji):
        st.write("Classified as: [  ", label, "  ] Confidence: ", output[0][0])
        for i in range(1, num_probs):
            st.markdown(
                f'<span style="color:grey">{output[1][i]} - {output[0][i]}</span>',
                unsafe_allow_html=True,
            )

        if predict_sentiment:
            polarity_scores = get_naive_sentiment(input_to_analyze)

            st.markdown(
                """<hr style="height:5px;width:70%;border:none;color:#333;background-color:#333; margin-top:0; margin-bottom:0;" /> """,
                unsafe_allow_html=True,
            )
            score = polarity_scores["compound"]
            score_value = (
                ":green[Positive]"
                if score >= 0.2
                else ":red[Negative]"
                if score <= -0.2
                else ":orange[Neutral]"
            )

            with st.container(border=True):
                st.write("Predicted sentiment: ", score_value, f" ({score})")
                st.write(
                    "Details: negative-",
                    polarity_scores["neg"],
                    " neutral-",
                    polarity_scores["neu"],
                    "positive-",
                    polarity_scores["pos"],
                )

        if extract_entities:
            st.markdown(
                """<hr style="height:5px;width:70%;border:none;color:#333;background-color:#333; margin-top:0; margin-bottom:0;" /> """,
                unsafe_allow_html=True,
            )

            ner_list = compute_ner(input_to_analyze)

            ner_list_dict = core.utils.get_ner_list_dict()

            with st.container(border=True):
                for i, ner_item in enumerate(ner_list):
                    if ner_item:
                        st.write("*", ner_list_dict[i])
                        for text in ner_item:
                            st.button(
                                text,
                                on_click=core.utils.set_state,
                                args=("selected_text", text),
                            )

                if any(item for item in ner_list):
                    st.success(
                        "You can click any of the phrases to search for them on the Wiki (BETA)"
                    )


if st.session_state.selected_text:
    with st.chat_message(name="human", avatar="🔍"):
        st.write("Phrase choosen:  " + st.session_state.selected_text)
    if not st.session_state.search_wiki:
        st.button("Search Wiki", on_click=core.utils.set_state, args=("search_wiki",))


if st.session_state.search_wiki:
    with st.spinner("..."):
        wiki_output = get_wikipedia_summary(st.session_state.selected_text)
        if wiki_output == "Page not found.":
            st.warning(
                wiki_output
                + " There might be an extra letter or a contraction in the phrase (e.g. 's). You can tweak it and search for it again or try a different review"
            )
            st.text_input(
                "Wiki user input",
                placeholder="Enter a review to be analyzed",
                label_visibility="collapsed",
                value=st.session_state.selected_text,
                key="wiki_user_input",
                max_chars=100,
                on_change=core.utils.wiki_user_input_fn,
            )

        else:
            with st.chat_message(name="human", avatar="📜"):
                st.write(wiki_output)
