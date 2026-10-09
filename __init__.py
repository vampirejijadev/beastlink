from .client import BeastlinkClient
from .player import Player
from .queue import Queue
from .extractor import Extractor
from .sources import detect_source, is_url
from .errors import BeastlinkError, PlayerError

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = [
    "BeastlinkClient",
    "Player",
    "Queue",
    "Extractor",
    "detect_source",
    "is_url",
    "BeastlinkError",
    "PlayerError",
]