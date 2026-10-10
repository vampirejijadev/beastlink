import os

from .player import Player
from .errors import BeastlinkError


class BeastlinkClient:
    def __init__(self, bot=None, url=None, password=None):
        self.bot = bot
        self.players = {}

        self.url = url or os.environ.get("BEASTLINK_URL", "")
        self.password = password or os.environ.get("BEASTLINK_PASSWORD", "")

        self.server_client = None
        if self.url and self.password:
            try:
                from .server_client import ServerClient
                self.server_client = ServerClient(self.url, self.password)
                print(f"[Beastlink] Remote mode: {self.url}")
            except Exception as e:
                print(f"[Beastlink] ServerClient init failed: {e}")
        else:
            print("[Beastlink] Standalone mode")

    def get_player(self, guild_id):
        if guild_id not in self.players:
            self.players[guild_id] = Player(self.bot, guild_id)
        return self.players[guild_id]

    async def join(self, guild_id, channel):
        player = self.get_player(guild_id)
        await player.connect(channel)
        return player

    async def leave(self, guild_id):
        if guild_id in self.players:
            await self.players[guild_id].disconnect()
            del self.players[guild_id]

    async def play(self, guild_id, query):
        if guild_id not in self.players:
            raise BeastlinkError("Bot is not connected to a voice channel")
        player = self.players[guild_id]
        return await player.play(query)

    async def pause(self, guild_id):
        if guild_id in self.players:
            return await self.players[guild_id].pause()
        return False

    async def resume(self, guild_id):
        if guild_id in self.players:
            return await self.players[guild_id].resume()
        return False

    async def skip(self, guild_id):
        if guild_id in self.players:
            return await self.players[guild_id].skip()
        return False

    async def stop(self, guild_id):
        if guild_id in self.players:
            return await self.players[guild_id].stop()
        return False

    def set_volume(self, guild_id, value):
        if guild_id in self.players:
            return self.players[guild_id].set_volume(value)
        return None

    def set_filter(self, guild_id, name):
        if guild_id in self.players:
            self.players[guild_id].set_filter(name)

    def set_loop(self, guild_id, mode):
        if guild_id in self.players:
            self.players[guild_id].set_loop(mode)

    def set_autoplay(self, guild_id, state):
        if guild_id in self.players:
            self.players[guild_id].set_autoplay(state)

    async def close(self):
        if self.server_client:
            try:
                await self.server_client.close()
            except Exception:
                pass