import streamlit as st
import spacy
from typing import List


@st.cache_resource
def get_ner():
    return spacy.load("en_core_web_sm")


def compute_ner(input: str) -> List[List[str]]:
    ner = get_ner()

    works_of_art, people, products, locations, orgs = [], [], [], [], []

    for ent in ner(input).ents:
        if ent.label_ == "WORK_OF_ART":
            works_of_art.append(ent.text)
        elif ent.label_ == "PERSON":
            people.append(ent.text)
        elif ent.label_ == "PRODUCT":
            products.append(ent.text)
        elif ent.label_ == "LOC":
            locations.append(ent.text)
        elif ent.label_ == "ORG":
            orgs.append(ent.text)

    return [works_of_art, people, products, locations, orgs]
