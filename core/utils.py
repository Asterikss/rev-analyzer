import streamlit as st
from typing import Dict, List
import base64
from enum import Enum
import nltk
import os
import json


def get_id2label_dict() -> Dict[int, str]:
    return {
        0: "magazines",
        1: "camera_photo",
        2: "office_products",
        3: "kitchen",
        4: "cell_phones_service",
        5: "computer_video_games",
        6: "grocery_and_gourmet_food",
        7: "tools_hardware",
        8: "automotive",
        9: "music_album",
        10: "health_and_personal_care",
        11: "electronics",
        12: "outdoor_living",
        13: "video",
        14: "apparel",
        15: "toys_games",
        16: "sports_outdoors",
        17: "books",
        18: "software",
        19: "baby",
        20: "musical_and_instruments",
        21: "beauty",
        22: "jewelry_and_watches",
    }


def get_lbl_emoji_dict() -> Dict[str, str]:
    return {
        "music_album": "🎧",
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


def get_ner_list_dict():
    return {
        0: "Works of art found:",
        1: "People mentioned:",
        2: "Phrases found:",
    }


def get_predefined_options() -> List[str]:
    return [
        "Red Hot Chili Peppers on vinyl has been a disappointing experience.. I had to return both “By The Way” and “Stadium Arcadium” because there were skips on almost all of it.. Kind of made it seem like the record label just went cheap, which is a disservice to anyone that actually listens to their vinyl...This “Greatest Hits” compilation did not have the same problems as the other two I bought. It sounded as it should have, and there were no skips.",
        "I've read a number of Stephen King's works over the past 15 years. King has always genuinely impressed me with his incredible eye for detail, his sense of place, and his ability to steadily pay out the rope line of a story's plot. Additionally, of course, he's the Jedi Master of creepiness. Although I was familiar with the premise of “The Stand”, it still scared me a lot.",
        "I recently purchased the “Arctic” honey from the Nature's Bounty Grocery Store. This product is not just a mere sweetener; it's a culinary adventure. The rich, golden texture and the sublime, natural flavor of this honey transported me to the lush fields of New Zealand, where it's ethically sourced. I've used it in various recipes, and each time, it has elevated my dishes to a new level of excellence.",
    ]


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_page_bg_data(page: str) -> str:
    if page == "Analyzer":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-position: center; 
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/blue_bird.jpg")}");
            background-position: top; 
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        </style>
        """
        # Use this to remove the empty space on top of the page
        # #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        #
        # Use this to remove "Deploy button (if header visibility is turned on"
        # .stDeployButton {{
        #         visibility: hidden;
        #     }}
        # This hids those stupid anchors ... but also removes pages from sidebar
        # /* Hide the link button https://discuss.streamlit.io/t/hide-titles-link/19783/13 */
        # .stApp a:first-child {{
        #     display: none;
        # }}
    elif page == "DataExplorer":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-position: center; 
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}
        </style>
        """
    return ""


def clear_memory(register: str):
    if register == "selected_text":
        st.session_state.selected_text = ""
        st.session_state.search_wiki = False
    else:
        st.session_state.selected_text = ""
        st.session_state.user_input = ""
        st.session_state.search_wiki = False


def set_state(state, content=None):
    if state == "selected_text":
        if content == None:
            st.warning(
                "When setting selected_text the content variable shouldn't be None"
            )
        else:
            st.session_state.selected_text = content
    elif state == "search_wiki":
        st.session_state.search_wiki = True
    else:
        st.warning(f"This state does not exist (set_state(), {state}")


def wiki_user_input_fn():
    st.session_state.search_wiki = False
    st.session_state.selected_text = st.session_state.wiki_user_input


def initialize(page: str) -> None:
    if page == "Analyzer":
        st.set_page_config(
            page_title="ReviewAnalyzer",
            page_icon="🔬",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("Analyzer"), unsafe_allow_html=True)
        if "selected_text" not in st.session_state:
            st.session_state.selected_text = ""
        if "search_wiki" not in st.session_state:
            st.session_state.search_wiki = False
    elif page == "DataExplorer":
        st.set_page_config(
            page_title="DataExplorer",
            page_icon="📖",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("DataExplorer"), unsafe_allow_html=True)


class Model(Enum):
    LR = 1
    NB = 2
    SVM = 3


@st.cache_data
def get_vc_classificatioin_dict() -> Dict:
    return {
        "Class": [
            "magazines",
            "camera_photo",
            "office_products",
            "kitchen",
            "cell_phones_service",
            "computer_video_games",
            "grocery_and_gourmet_food",
            "tools_hardware",
            "automotive",
            "music_album",
            "health_and_personal_care",
            "electronics",
            "outdoor_living",
            "video",
            "apparel",
            "toys_games",
            "sports_outdoors",
            "books",
            "software",
            "baby",
            "musical_and_instruments",
            "beauty",
            "jewelry_and_watches",
        ],
        "Frequency": [
            779,
            821,
            122,
            774,
            351,
            604,
            934,
            4,
            233,
            832,
            763,
            787,
            488,
            851,
            672,
            830,
            799,
            854,
            699,
            570,
            73,
            587,
            393,
        ],
    }


def get_len_bins_classification_dict() -> Dict:
    return {
        "Bin": [
            "(0, 200]",
            "(200, 300]",
            "(300, 400]",
            "(400, 500]",
            "(500, 600]",
            "(600, 700]",
            "(700, 800]",
            "(800, 900]",
            "(900, 1000]",
            "(1000, 1500]",
            "(1500, 2000]",
            "(2000, 5000]",
            "(5000, 10000]",
            "(10000, 20000]",
            "(20000, 31154]",
        ],
        "Frequency": [
            1361,
            2622,
            2149,
            1711,
            1232,
            896,
            725,
            536,
            433,
            1142,
            450,
            508,
            47,
            7,
            1,
        ],
    }


def download_nltk_packages() -> None:
    nltk.data.path.append(os.getcwd() + "/nltk_data")
    try:
        nltk.find("corpora/wordnet.zip")
        print("Wordnet found")
    except LookupError:
        nltk.download("wordnet")
        print("Wordnet not found. Downloading...")

    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
        print("Vader_lexicon found")
    except LookupError:
        nltk.download("vader_lexicon")
        print("Vader_lexicon not found. Downloading...")

    try:
        nltk.data.find("corpora/stopwords.zip")
        print("Stopwords found")
    except LookupError:
        nltk.download("stopwords")
        print("Stopwords not found. Downloading...")

    st.session_state.check_packages_once = "MariuszPudzianowski"


@st.cache_data
def load_lottiefile(path: str):
    with open(path) as f:
        return json.load(f)
