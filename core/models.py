import streamlit as st
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F # TODO maby write softmax
from typing import Tuple, List

from core.utils import get_id2label_dict 


@st.cache_resource
def get_classifier():
    return (AutoModelForSequenceClassification.from_pretrained("Asteriks/distilbert-cased-reviews-v1"),
            AutoTokenizer.from_pretrained("Asteriks/distilbert-cased-reviews-v1"))


def query_classifier(input: str) -> Tuple[List[float], List[str]]:
    classifier_model, tokenizer = get_classifier()

    out = classifier_model(**(tokenizer(input, return_tensors="pt")))
    probs = F.softmax(out.logits, dim=-1)[0].tolist()
    sorted_probs, sorted_idxs = zip(*sorted(zip(probs, range(len(probs))), reverse=True))
    id2label_dict = get_id2label_dict()

    return sorted_probs, [id2label_dict[idx] for idx in sorted_idxs]
