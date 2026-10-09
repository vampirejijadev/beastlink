import sys
sys.path.insert(0, "/storage/emulated/0/Download")

print("Testing Beastlink v2 (self-contained)...")
print()

try:
    from beastlink import BeastlinkClient
    print("client OK")
except Exception as e:
    print("client FAILED:", e)

try:
    from beastlink.player import Player
    print("player OK")
except Exception as e:
    print("player FAILED:", e)

try:
    from beastlink.queue import Queue
    print("queue OK")
except Exception as e:
    print("queue FAILED:", e)

try:
    from beastlink.extractor import Extractor
    print("extractor OK")
except Exception as e:
    print("extractor FAILED:", e)

try:
    from beastlink.sources import detect_source, is_url
    print("sources OK")
    print("  detect youtube:", detect_source("https://youtube.com/watch?v=abc"))
    print("  detect spotify:", detect_source("https://open.spotify.com/track/xyz"))
    print("  detect search:", detect_source("never gonna give you up"))
    print("  is_url:", is_url("https://youtu.be/abc"))
except Exception as e:
    print("sources FAILED:", e)

try:
    from beastlink.errors import BeastlinkError, PlayerError
    print("errors OK")
except Exception as e:
    print("errors FAILED:", e)

print()
print("Done.")