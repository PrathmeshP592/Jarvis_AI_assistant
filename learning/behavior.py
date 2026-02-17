# import json
# from collections import defaultdict
# from pathlib import Path

# PROFILE_FILE = Path("learning/user_profile.json")


# def load_profile():
#     if PROFILE_FILE.exists():
#         return json.loads(PROFILE_FILE.read_text())
#     return {
#         "verbosity": "short",
#         "topics": defaultdict(int),
#         "technical": 0
#     }


# def save_profile(profile):
#     PROFILE_FILE.parent.mkdir(exist_ok=True)
#     PROFILE_FILE.write_text(json.dumps(profile, indent=2))


# def analyze_interaction(user_input, response):
#     profile = load_profile()

#     # ---- verbosity learning ----
#     if len(response.split()) > 60:
#         profile["verbosity"] = "detailed"
#     else:
#         profile["verbosity"] = "short"

#     # ---- topic learning ----
#     for word in user_input.lower().split():
#         if len(word) > 4:
#             profile["topics"][word] = profile["topics"].get(word, 0) + 1

#     # ---- technical detection ----
#     tech_words = ["code", "python", "model", "ai", "data", "server", "api"]
#     if any(w in user_input.lower() for w in tech_words):
#         profile["technical"] += 1

#     save_profile(profile)


# def build_behavior_context():
#     profile = load_profile()

#     context = f"""
# User preferences:
# - Prefers {profile['verbosity']} responses
# - Often discusses: {sorted(profile['topics'], key=profile['topics'].get, reverse=True)[:5]}
# - Technical interest level: {profile['technical']}
# """

#     return context


import json
import re
from pathlib import Path

PROFILE_FILE = Path("learning/user_profile.json")

STOPWORDS = {
    "the","and","is","are","was","were","about","again","okay","yeah",
    "this","that","with","what","when","where","how","who","why",
    "today","right","actually","please","tell"
}

MAX_TOPICS = 20


def load_profile():
    if PROFILE_FILE.exists():
        return json.loads(PROFILE_FILE.read_text())
    return {
        "verbosity": "short",
        "topics": {},
        "technical": 0
    }


def save_profile(profile):
    PROFILE_FILE.parent.mkdir(exist_ok=True)
    PROFILE_FILE.write_text(json.dumps(profile, indent=2))


def clean_words(text):
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def decay_topics(topics):
    for k in list(topics.keys()):
        topics[k] *= 0.95
        if topics[k] < 0.3:
            del topics[k]


def trim_topics(topics):
    return dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)[:MAX_TOPICS])


def analyze_interaction(user_input, response):
    profile = load_profile()

    # ---- verbosity ----
    profile["verbosity"] = "detailed" if len(response.split()) > 60 else "short"

    # ---- topic learning ----
    words = clean_words(user_input)
    for w in words:
        profile["topics"][w] = profile["topics"].get(w, 0) + 1

    decay_topics(profile["topics"])
    profile["topics"] = trim_topics(profile["topics"])

    # ---- technical interest ----
    tech_words = ["code","python","model","ai","data","server","api","llm"]
    if any(w in user_input.lower() for w in tech_words):
        profile["technical"] += 1

    save_profile(profile)


def build_behavior_context():
    profile = load_profile()

    top_topics = list(profile["topics"].keys())

    return f"""
User preferences:
- Prefers {profile['verbosity']} answers
- Main interests: {top_topics}
- Technical interest level: {profile['technical']}
"""