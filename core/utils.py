import streamlit as st
from typing import Dict, List
import base64


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
        2: "Events mentioned:",
        3: "Products mentioned:",
        4: "Locations mentioned:",
        5: "Organizations mentioned:",
    }


def get_predefined_options() -> List[str]:
    return [
        "Red Hot Chili Peppers on vinyl has been a disappointing experience.. I had to return both “By The Way” and “Stadium Arcadium” because there were skips on almost all of it.. Kind of made it seem like the record label just went cheap, which is a disservice to anyone that actually listens to their vinyl...This “Greatest Hits” compilation did not have the same problems as the other two I bought. It sounded as it should have, and there were no skips.",
        "I've read a number of Stephen King's works over the past 15 years. King has always genuinely impressed me with his incredible eye for detail, his sense of place, and his ability to steadily pay out the rope line of a story's plot. Additionally, of course, he's the Jedi Master of creepiness. Although I was familiar with the premise of “The Stand”, it still scared me a lot",
    ]


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_page_bg_data() -> str:
    return f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stSidebar"] > div:first-child {{
        background-image: url("data:image/png;base64,{get_img_as_base64("images/dark_bg.jpg")}");
        background-position: center; 
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: top left;
    }}

    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{get_img_as_base64("images/blue_bird.jpg")}");
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


def initialize():
    st.set_page_config(page_title="ReviewAnalyzer", page_icon="🔬", layout="wide")
    st.markdown(get_page_bg_data(), unsafe_allow_html=True)
    if "selected_text" not in st.session_state:
        st.session_state.selected_text = ""
    if "search_wiki" not in st.session_state:
        st.session_state.search_wiki = False
