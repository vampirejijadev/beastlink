import time
import queue
import threading
import subprocess

import discord

from .extractor import ytdlp_stream_command, ffmpeg_command


class PipeSource(discord.AudioSource):
    def __init__(self, query, filter_arg=None):
        self.ytdlp = None
        self.ffmpeg = None
        self._closed = False
        self._buffer = queue.Queue(maxsize=2000)
        self._pending = b""
        self._reader_thread = None

        try:
            self.ytdlp = subprocess.Popen(
                ytdlp_stream_command(query),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.ffmpeg = subprocess.Popen(
                ffmpeg_command(filter_arg),
                stdin=self.ytdlp.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.ytdlp.stdout.close()

            self._reader_thread = threading.Thread(
                target=self._reader_loop,
                daemon=True,
            )
            self._reader_thread.start()

        except Exception as e:
            print(f"[PipeSource] Failed to start: {e}")
            self._closed = True
            self.cleanup()

    def wait_ready(self, timeout=15, min_bytes=3840 * 25):
        deadline = time.time() + timeout
        collected = []
        total = 0

        while time.time() < deadline:
            try:
                chunk = self._buffer.get(timeout=1)
            except queue.Empty:
                if self.ytdlp and self.ytdlp.poll() is not None:
                    try:
                        err = self.ytdlp.stderr.read().decode(errors="ignore")
                        if err:
                            print(f"[PipeSource] yt-dlp error: {err[:200]}")
                    except Exception:
                        pass
                    return False
                continue

            if not chunk:
                return False

            collected.append(chunk)
            total += len(chunk)

            if total >= min_bytes:
                for c in collected:
                    self._buffer.put(c)
                return True

        if collected:
            for c in collected:
                self._buffer.put(c)
            return True

        return False

    def _reader_loop(self):
        try:
            while not self._closed:
                data = self.ffmpeg.stdout.read(38400)
                if not data:
                    break
                self._buffer.put(data)
        except Exception:
            pass
        finally:
            try:
                self._buffer.put_nowait(b"")
            except Exception:
                pass

    def read(self):
        if self._closed:
            return b""

        try:
            while len(self._pending) < 3840:
                try:
                    data = self._buffer.get(timeout=10)
                except queue.Empty:
                    return b""

                if not data:
                    self._closed = True
                    return b""

                self._pending += data

            chunk = self._pending[:3840]
            self._pending = self._pending[3840:]
            return chunk

        except Exception:
            self._closed = True
            return b""

    def is_opus(self):
        return False

    def cleanup(self):
        self._closed = True
        for proc in (self.ytdlp, self.ffmpeg):
            if proc:
                try:
                    proc.kill()
                except Exception:
                    pass