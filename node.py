import asyncio
from .errors import NodeConnectionError


class Node:
    def __init__(self, uri, password, name="beast-node"):
        self.uri = uri
        self.password = password
        self.name = name
        self.connected = False
        self.session = None

    async def connect(self):
        try:
            self.connected = True
            return True
        except Exception as e:
            raise NodeConnectionError(f"Failed to connect to {self.name}: {e}")

    async def disconnect(self):
        self.connected = False
        self.session = None

    def is_connected(self):
        return self.connected