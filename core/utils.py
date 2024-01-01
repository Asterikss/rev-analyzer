from typing import Dict, List


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


def get_predefined_options() -> List[str]:
    return [
        "Red Hot Chili Peppers on vinyl has been a disappointing experience.. I had to return both “By The Way” and “Stadium Arcadium” because there were skips on almost all of it.. Kind of made it seem like the record label just went cheap, which is a disservice to anyone that actually listens to their vinyl...This “Greatest Hits” compilation did not have the same problems as the other two I bought. It sounded as it should have, and there were no skips.",
        "I've read a number of Stephen King's works over the past 15 years. King has always genuinely impressed me with his incredible eye for detail, his sense of place, and his ability to steadily pay out the rope line of a story's plot. Additionally, of course, he's the Jedi Master of creepiness. Although I was familiar with the premise of “The Stand”, it still scared me a lot",
    ]
