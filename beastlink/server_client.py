import os
import json
import urllib.request
import urllib.parse


class ServerClient:
    def __init__(self, url, password):
        self.url = url.rstrip("/")
        self.password = password

    def _request(self, method, path, body=None, timeout=15):
        url = f"{self.url}{path}"
        data = None
        headers = {
            "X-Beastlink-Password": self.password,
        }

        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method,
        )

        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode()
            try:
                return json.loads(raw)
            except Exception:
                return {"raw": raw}

    async def ping(self):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._request, "GET", "/ping"
        )

    async def extract(self, query):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._request,
            "POST",
            "/extract",
            {"query": query},
        )

    def stream_url(self, vid):
        return f"{self.url}/stream/{vid}?password={urllib.parse.quote(self.password)}"

    async def close(self):
        pass