import streamlit as st
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from typing import Tuple, List
from math import exp

from core.utils import get_id2label_dict


@st.cache_resource
def get_classifier():
    return (
        AutoModelForSequenceClassification.from_pretrained(
            "Asteriks/distilbert-cased-reviews-v1"
        ),
        AutoTokenizer.from_pretrained("Asteriks/distilbert-cased-reviews-v1"),
    )


def custom_softmax(logits):
    max_val = max(logits)
    exps = [exp(logit - max_val) for logit in logits]
    exps_sum = sum(exps)
    return [exp / exps_sum for exp in exps]


def query_classifier(input: str) -> Tuple[List[float], List[str]]:
    classifier_model, tokenizer = get_classifier()

    out = classifier_model(**(tokenizer(input, return_tensors="pt")))
    # probs = F.softmax(out.logits, dim=-1)[0].tolist()
    probs = custom_softmax(out.logits[0])

    sorted_probs, sorted_idxs = zip(
        *sorted(zip(probs, range(len(probs))), reverse=True)
    )
    id2label_dict = get_id2label_dict()

    return sorted_probs, [id2label_dict[idx] for idx in sorted_idxs]
