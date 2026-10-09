import discord

from .player import Player
from .extractor import Extractor
from .errors import BeastlinkError


class BeastlinkClient:
    def __init__(self, bot=None):
        self.bot = bot
        self.players = {}
        self.extractor = Extractor()

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

    async def search(self, query, limit=10):
        return await self.extractor.extract_many(query, limit)