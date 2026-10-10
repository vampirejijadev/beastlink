from .client import BeastlinkClient
from .player import Player
from .queue import Queue
from .pipesource import PipeSource
from .extractor import Extractor
from .sources import detect_source, is_url
from .filters import FILTERS, apply_filter
from .autoinstall import run_autofix
from .errors import (
    BeastlinkError,
    PlayerError,
    NodeConnectionError,
    ServerAuthError,
)

__version__ = "0.2.2"
__author__ = "VampireDev"

__all__ = [
    "BeastlinkClient",
    "Player",
    "Queue",
    "PipeSource",
    "Extractor",
    "detect_source",
    "is_url",
    "FILTERS",
    "apply_filter",
    "run_autofix",
    "BeastlinkError",
    "PlayerError",
    "NodeConnectionError",
    "ServerAuthError",
]
