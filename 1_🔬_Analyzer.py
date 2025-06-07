import streamlit as st

import core.utils
from core.utils import Model
from core.models import query_classifier
from core.named_entity_recognition import compute_ner
from core.wiki_service import get_wikipedia_summary
from core.sentiment import get_sentiment_prediction, get_naive_sentiment
from core.word_vectors import plot_words

core.utils.initialize("Analyzer")

if "check_packages_once" not in st.session_state:
  core.utils.download_nltk_packages()

st.title(":blue[ReviewAnalyzer]", anchor=False)

with st.sidebar:
  predict_sentiment = st.toggle("Predict sentiment", value=True)
  plot_words_bt = st.toggle("Plot words", value=True)
  extract_entities = st.toggle("Extract entities", value=True)
  num_probs = st.slider("How many probabilities to display?", 1, 4, 1)
  with st.expander("Models in use"):
    if predict_sentiment:
      naive = st.toggle("Naive prediction", value=True)
      lr = st.toggle("Linear regression", value=True)
      nbayes = st.toggle("Naive Bayes", value=True)
      svm = st.toggle("SVM", value=True)
    else:
      naive = st.toggle("Naive prediction", value=False, disabled=True)
      lr = st.toggle("Linear regression", value=False, disabled=True)
      nbayes = st.toggle("Naive Bayes", value=False, disabled=True)
      svm = st.toggle("SVM", value=False, disabled=True)
    st.info(
      'Info: All models (not including "Naive prediction") can only output Positive or Negative.'
    )
  with st.expander("Plot words"):
    normalize_wv = st.toggle(
      "Normalize word vectors before casting them to lower dimension", value=True
    )
  with st.expander("Additional settings"):
    if predict_sentiment:
      values_slider = st.slider(
        'Select a range for "Neutral" for naive sentiment analysis',
        -0.9,
        0.9,
        (-0.2, 0.2),
        step=0.1,
      )
    else:
      values_slider = (-0.2, 0.2)

  st.markdown(
    """
        <a href="https://github.com/Asterikss/rev-analyzer" title="Git"><img src="https://img.shields.io/badge/-black?logo=github&link=https%3A%2F%2Fgithub.com%2FAsterikss%2Frev-analyzer" style="height:28px; width:auto;"></a>
        """,
    unsafe_allow_html=True,
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

st.text_area(
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

    if predict_sentiment and any([lr, naive, nbayes]):
      st.markdown(
        """<hr style="height:5px;width:70%;border:none;color:#333;background-color:#333; margin-top:0; margin-bottom:0;" /> """,
        unsafe_allow_html=True,
      )

      with st.container(border=True):
        st.write("*", "Predicted sentiment:")
        if naive:
          polarity_scores = get_naive_sentiment(input_to_analyze)

          score = polarity_scores["compound"]

          score_value = (
            ":green[Positive]"
            if score >= values_slider[1]
            else ":red[Negative]"
            if score <= values_slider[0]
            else ":orange[Neutral]"
          )
          st.write(
            "Naive prediction: ",
            score_value,
            f" ({score})",
            "Details: negative-",
            polarity_scores["neg"],
            " neutral-",
            polarity_scores["neu"],
            "positive-",
            polarity_scores["pos"],
          )

        if lr:
          st.write(
            f"Linear regression: {':green[Positive]' if get_sentiment_prediction(input_to_analyze, Model.LR) == 1.0 else ':red[Negative]'}"
          )

        if nbayes:
          st.write(
            f"Naive Bayes: {':green[Positive]' if get_sentiment_prediction(input_to_analyze, Model.NB) == 1.0 else ':red[Negative]'}"
          )

        if svm:
          st.write(
            f"Support Vector Machine: {':green[Positive]' if get_sentiment_prediction(input_to_analyze, Model.SVM) == 1.0 else ':red[Negative]'}"
          )

    if plot_words_bt:
      st.markdown(
        """<hr style="height:5px;width:70%;border:none;color:#333;background-color:#333; margin-top:0; margin-bottom:0;" /> """,
        unsafe_allow_html=True,
      )

      with st.container(border=True):
        plot_words(input_to_analyze, normalize_wv)

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
            "You can click any of the phrases to search for them using Wiki corpuse (BETA)"
          )


if st.session_state.selected_text:
  with st.chat_message(name="human", avatar="🔍"):
    st.write("Chosen phrase:  " + st.session_state.selected_text)
  if not st.session_state.search_wiki:
    st.button("Search Wiki", on_click=core.utils.set_state, args=("search_wiki",))


if st.session_state.search_wiki:
  with st.spinner("..."):
    wiki_output = get_wikipedia_summary(st.session_state.selected_text)
    if wiki_output == "Page not found.":
      st.warning(
        wiki_output
        + " There might be an extra letter or a contraction in the phrase (e.g. 's). Or it might not exist. You can tweak it and search for it again or try a different review"
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
