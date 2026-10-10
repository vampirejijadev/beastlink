import asyncio

from .queue import Queue
from .pipesource import PipeSource
from .filters import apply_filter
from .errors import PlayerError


class Player:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.queue = Queue()
        self.voice_client = None
        self.current = None
        self.volume = 1.0
        self.loop = 0
        self.filter = None
        self.autoplay = False
        self._gen = 0
        self._source = None
        self._prefetch = None

    def _is_playing(self):
        return bool(
            self.voice_client
            and (
                self.voice_client.is_playing()
                or self.voice_client.is_paused()
            )
        )

    async def connect(self, channel):
        if self.voice_client and self.voice_client.is_connected():
            if self.voice_client.channel != channel:
                await self.voice_client.move_to(channel)
            return self.voice_client

        self.voice_client = await channel.connect(
            self_deaf=True,
            timeout=10,
        )
        return self.voice_client

    async def disconnect(self):
        self._gen += 1
        self._cleanup_source()
        self._cleanup_prefetch()

        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()

        self.voice_client = None
        self.current = None
        await self.queue.clear()

    def _cleanup_source(self):
        if self._source:
            try:
                self._source.cleanup()
            except Exception:
                pass
            self._source = None

    def _cleanup_prefetch(self):
        if self._prefetch:
            try:
                self._prefetch["source"].cleanup()
            except Exception:
                pass
            self._prefetch = None

    async def play(self, query):
        track = {"query": query, "title": query}
        await self.queue.add(track)

        if self._is_playing():
            self._trigger_prefetch()
        else:
            self._gen += 1
            self._cleanup_source()
            await self._play_next()

        return track

    def _trigger_prefetch(self):
        if self._prefetch:
            return
        if self.queue.is_empty():
            return

        nxt = self.queue.peek()

        try:
            asyncio.run_coroutine_threadsafe(
                self._do_prefetch(nxt),
                self.bot.loop,
            )
        except Exception:
            pass

    async def _do_prefetch(self, track):
        if self._prefetch:
            return

        try:
            loop = asyncio.get_event_loop()
            print(f"[Player] Prefetching: {track['query']}")

            f_arg = apply_filter(self.filter)

            source = await loop.run_in_executor(
                None,
                PipeSource,
                track["query"],
                f_arg,
            )

            ready = await loop.run_in_executor(
                None,
                source.wait_ready,
                20,
                3840 * 50,
            )

            if ready:
                self._prefetch = {
                    "query": track["query"],
                    "source": source,
                }
                print(f"[Player] Prefetched: {track['query']}")
            else:
                source.cleanup()
                print(f"[Player] Prefetch failed: {track['query']}")

        except Exception as e:
            print(f"[Player] Prefetch error: {e}")

    async def _play_next(self):
        if not self.voice_client or not self.voice_client.is_connected():
            return

        if self.queue.is_empty():
            self.current = None
            return

        self.current = await self.queue.get()
        self._gen += 1
        my_gen = self._gen
        self._cleanup_source()

        if (
            self._prefetch
            and self._prefetch["query"] == self.current["query"]
        ):
            print(f"[Player] PREFETCHED: {self.current['query']}")
            self._source = self._prefetch["source"]
            self._prefetch = None
        else:
            print(f"[Player] Streaming: {self.current['query']}")
            try:
                loop = asyncio.get_event_loop()
                f_arg = apply_filter(self.filter)

                self._source = await loop.run_in_executor(
                    None,
                    PipeSource,
                    self.current["query"],
                    f_arg,
                )

                ready = await loop.run_in_executor(
                    None,
                    self._source.wait_ready,
                    20,
                    3840 * 50,
                )

                if not ready:
                    print(f"[Player] No data received")
                    self._source.cleanup()
                    self._source = None
                    await self._play_next()
                    return

            except Exception as e:
                print(f"[Player] Failed: {e}")
                self._source = None
                await self._play_next()
                return

        try:
            self.voice_client.play(
                self._source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self._after_play(e, my_gen),
                    self.bot.loop,
                ),
            )
        except Exception as e:
            print(f"[Player] Play error: {e}")
            self._cleanup_source()
            await self._play_next()
            return

        self._trigger_prefetch()

    async def _after_play(self, error, gen):
        if gen != self._gen:
            return

        if error:
            print(f"[Player] Playback error: {error}")

        self._cleanup_source()

        if self.loop == 1 and self.current:
            await self.queue.add(self.current)
        elif self.loop == 2 and self.current:
            await self.queue.add(self.current)

        await self._play_next()

    async def skip(self):
        self._gen += 1
        self._cleanup_source()

        if self.voice_client and (
            self.voice_client.is_playing()
            or self.voice_client.is_paused()
        ):
            self.voice_client.stop()
            await asyncio.sleep(0.5)

        if not self.queue.is_empty():
            await self._play_next()
        else:
            self.current = None

    async def stop(self):
        await self.queue.clear()
        self._gen += 1
        self._cleanup_source()
        self._cleanup_prefetch()

        if self.voice_client and (
            self.voice_client.is_playing()
            or self.voice_client.is_paused()
        ):
            self.voice_client.stop()
            await asyncio.sleep(0.3)

        self.current = None

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

    def set_volume(self, value):
        if value < 0 or value > 2.0:
            raise PlayerError("Volume must be between 0.0 and 2.0")
        self.volume = value
        return value

    def set_filter(self, name):
        self.filter = name

    def set_loop(self, mode):
        self.loop = int(mode) % 3

    def set_autoplay(self, state):
        self.autoplay = bool(state)

    def is_playing(self):
        return self._is_playing()

    def is_paused(self):
        if self.voice_client:
            return self.voice_client.is_paused()
        return False