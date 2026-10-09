import re


YOUTUBE_PATTERNS = [
    r"youtube\.com/watch\?v=",
    r"youtu\.be/",
    r"youtube\.com/shorts/",
]

YOUTUBE_MUSIC_PATTERNS = [
    r"music\.youtube\.com/",
]

SPOTIFY_PATTERNS = [
    r"open\.spotify\.com/",
]

SOUNDCLOUD_PATTERNS = [
    r"soundcloud\.com/",
]

APPLE_MUSIC_PATTERNS = [
    r"music\.apple\.com/",
]

DEEZER_PATTERNS = [
    r"deezer\.com/",
]


def _matches(patterns, text):
    for p in patterns:
        if re.search(p, text):
            return True
    return False


def detect_source(query):
    q = query.lower()

    if _matches(YOUTUBE_MUSIC_PATTERNS, q):
        return "youtubemusic"
    if _matches(YOUTUBE_PATTERNS, q):
        return "youtube"
    if _matches(SPOTIFY_PATTERNS, q):
        return "spotify"
    if _matches(SOUNDCLOUD_PATTERNS, q):
        return "soundcloud"
    if _matches(APPLE_MUSIC_PATTERNS, q):
        return "applemusic"
    if _matches(DEEZER_PATTERNS, q):
        return "deezer"

    return "search"


def is_url(query):
    return query.startswith("http://") or query.startswith("https://")


def search_term(query):
    if is_url(query):
        return query
    return f"ytsearch1:{query}"