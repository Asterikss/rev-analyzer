import streamlit as st
import spacy

@st.cache_resource
def get_ner():
    return spacy.load("en_core_web_sm")

def compute_ner(input: str):
    ner = get_ner()
    works_of_art = []
    people = []
    for ent in ner(input).ents:
        if (ent.label_ not in ["WORK_OF_ART", "PERSON"]):
            st.warning(f"some ent.label_s are not yet implemented {ent.text} {ent.label_}")

        if ent.label_ == "WORK_OF_ART":
            works_of_art.append(ent.text)
        elif ent.label_ == "PERSON":
            people.append(ent.text)

    return works_of_art, people
