import re

PATTERNS = {
    "youtubemusic": [r"music\.youtube\.com/"],
    "youtube": [
        r"youtube\.com/watch\?v=",
        r"youtu\.be/",
        r"youtube\.com/shorts/",
    ],
    "spotify": [r"open\.spotify\.com/"],
    "soundcloud": [r"soundcloud\.com/"],
    "applemusic": [r"music\.apple\.com/"],
    "deezer": [r"deezer\.com/"],
    "twitch": [r"twitch\.tv/"],
    "bandcamp": [r"bandcamp\.com/"],
}


def detect_source(query):
    q = query.lower()
    for name, pats in PATTERNS.items():
        for p in pats:
            if re.search(p, q):
                return name
    return "search"


def is_url(query):
    return query.startswith("http://") or query.startswith("https://")


def search_term(query):
    if is_url(query):
        return query
    return f"ytsearch1:{query}"