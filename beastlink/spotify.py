import os
import json
import urllib.request
import urllib.parse
import base64


class SpotifyClient:
    def __init__(self, client_id=None, client_secret=None):
        self.client_id = client_id or os.environ.get("SPOTIFY_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("SPOTIFY_CLIENT_SECRET", "")
        self._token = None

    def _get_token(self):
        if self._token:
            return self._token

        if not (self.client_id and self.client_secret):
            raise Exception("Spotify credentials missing")

        auth = f"{self.client_id}:{self.client_secret}"
        auth_b64 = base64.b64encode(auth.encode()).decode()

        req = urllib.request.Request(
            "https://accounts.spotify.com/api/token",
            data=b"grant_type=client_credentials",
            headers={
                "Authorization": f"Basic {auth_b64}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())

        self._token = data.get("access_token")
        return self._token

    def search_track(self, query):
        token = self._get_token()
        qs = urllib.parse.urlencode({"q": query, "type": "track", "limit": 1})
        req = urllib.request.Request(
            f"https://api.spotify.com/v1/search?{qs}",
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())

        items = data.get("tracks", {}).get("items", [])
        if not items:
            return None

        t = items[0]
        artists = ", ".join(a["name"] for a in t.get("artists", []))
        return {
            "title": t.get("name", "Unknown"),
            "artist": artists or "Unknown",
            "search_query": f"{artists} {t.get('name', '')}".strip(),
        }