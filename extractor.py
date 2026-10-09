import asyncio
import yt_dlp

from .errors import BeastlinkError
from .sources import is_url, search_term


YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch1",
    "noplaylist": True,
    "extract_flat": False,
}


class Extractor:
    def __init__(self, options=None):
        self.options = options or YTDL_OPTIONS
        self.ytdl = yt_dlp.YoutubeDL(self.options)

    async def extract(self, query):
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(None, self._extract_sync, query)
        except Exception as e:
            raise BeastlinkError(f"Extraction failed: {e}")

    def _extract_sync(self, query):
        target = query if is_url(query) else search_term(query)
        info = self.ytdl.extract_info(target, download=False)

        if "entries" in info:
            if not info["entries"]:
                raise BeastlinkError("No results found")
            info = info["entries"][0]

        return {
            "title": info.get("title", "Unknown"),
            "url": info.get("url"),
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url"),
            "uploader": info.get("uploader", "Unknown"),
        }

    async def extract_many(self, query, limit=10):
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(
                None, self._extract_many_sync, query, limit
            )
        except Exception as e:
            raise BeastlinkError(f"Extraction failed: {e}")

    def _extract_many_sync(self, query, limit):
        target = f"ytsearch{limit}:{query}"
        info = self.ytdl.extract_info(target, download=False)

        results = []
        for entry in info.get("entries", []):
            if not entry:
                continue
            results.append({
                "title": entry.get("title", "Unknown"),
                "url": entry.get("url"),
                "duration": entry.get("duration", 0),
                "thumbnail": entry.get("thumbnail"),
                "webpage_url": entry.get("webpage_url"),
                "uploader": entry.get("uploader", "Unknown"),
            })
        return results