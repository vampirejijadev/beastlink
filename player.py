import asyncio
import discord

from .queue import Queue
from .extractor import Extractor
from .errors import PlayerError


FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


class Player:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.queue = Queue()
        self.extractor = Extractor()
        self.voice_client = None
        self.current = None
        self.volume = 1.0
        self.loop = False
        self._playing = False

    async def connect(self, channel):
        if self.voice_client and self.voice_client.is_connected():
            if self.voice_client.channel != channel:
                await self.voice_client.move_to(channel)
            return self.voice_client

        self.voice_client = await channel.connect()
        return self.voice_client

    async def disconnect(self):
        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()
        self.voice_client = None
        self._playing = False

    async def play(self, query):
        track = await self.extractor.extract(query)
        await self.queue.add(track)

        if not self._playing:
            await self._play_next()

        return track

    async def _play_next(self):
        if self.voice_client is None or not self.voice_client.is_connected():
            raise PlayerError("Not connected to a voice channel")

        if self.queue.is_empty():
            self._playing = False
            self.current = None
            return

        self.current = await self.queue.get()
        self._playing = True

        source = discord.FFmpegPCMAudio(
            self.current["url"],
            **FFMPEG_OPTIONS
        )

        if self.volume != 1.0:
            source = discord.PCMVolumeTransformer(source, volume=self.volume)

        self.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self._after_play(e), self.bot.loop
            )
        )

    async def _after_play(self, error):
        if self.loop and self.current:
            await self.queue.add(self.current)

        if error:
            print(f"Playback error: {error}")

        await self._play_next()

    async def pause(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            return True
        return False

    async def resume(self):
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            return True
        return False

    async def skip(self):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            return True
        return False

    async def stop(self):
        await self.queue.clear()
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
        self._playing = False
        self.current = None
        return True

    def set_volume(self, value):
        if value < 0 or value > 2.0:
            raise PlayerError("Volume must be between 0.0 and 2.0")
        self.volume = value
        if self.voice_client and self.voice_client.source:
            self.voice_client.source.volume = value
        return value

    def set_loop(self, state):
        self.loop = bool(state)
        return self.loop

    def is_playing(self):
        return self._playing

    def is_paused(self):
        return self.voice_client.is_paused() if self.voice_client else False