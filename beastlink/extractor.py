import os
import sys
import subprocess
import json

from .autoinstall import NODE_BIN, COOKIE_FILE


UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def _node_path():
    if os.path.isfile(NODE_BIN):
        return NODE_BIN
    return None


def _base_flags():
    flags = ["--user-agent", UA]
    n = _node_path()
    if n:
        flags.extend(["--js-runtimes", f"node:{n}"])
    if os.path.isfile(COOKIE_FILE):
        flags.extend(["--cookies", COOKIE_FILE])
    return flags


def _target(query):
    if query.startswith("http://") or query.startswith("https://"):
        return query
    return f"ytsearch1:{query}"


def ytdlp_stream_command(query):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bestaudio/best",
        "--no-playlist",
        "-o", "-",
        "--quiet",
        "--no-warnings",
        "--no-part",
        "--no-cache-dir",
        "--socket-timeout", "15",
        "--retries", "5",
    ]
    cmd.extend(_base_flags())
    cmd.append(_target(query))
    return cmd


def ytdlp_meta_command(query):
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--dump-json",
        "--no-playlist",
        "--quiet",
        "--no-warnings",
        "--socket-timeout", "15",
    ]
    cmd.extend(_base_flags())
    cmd.append(_target(query))
    return cmd


def ffmpeg_command(filter_arg=None):
    cmd = ["ffmpeg", "-re", "-i", "pipe:0"]
    if filter_arg:
        cmd.extend(["-af", filter_arg])
    cmd.extend([
        "-f", "s16le",
        "-ar", "48000",
        "-ac", "2",
        "-loglevel", "error",
        "pipe:1",
    ])
    return cmd


class Extractor:
    def __init__(self, options=None):
        pass

    async def extract(self, query):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync, query)

    def _sync(self, query):
        r = subprocess.run(
            ytdlp_meta_command(query),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r.returncode != 0:
            raise Exception(r.stderr[:300])

        info = json.loads(r.stdout)

        return {
            "title": info.get("title", "Unknown"),
            "vid": info.get("id", ""),
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url") or query,
            "uploader": info.get("uploader", "Unknown"),
        }