import os
import sys
import shutil
import subprocess


NODE_BIN = "/home/container/bin/node"
COOKIE_FILE = "/home/container/cookies.txt"
CACHE_DIR = "/home/container/music_cache"


def cleanup_disk():
    for p in [
        "/home/container/bgutil-server",
        "/home/container/.cache",
        "/root/.cache",
        "/home/container/.npm",
    ]:
        shutil.rmtree(p, ignore_errors=True)
    try:
        for f in os.listdir("/tmp"):
            try:
                fp = f"/tmp/{f}"
                if os.path.isfile(fp):
                    os.remove(fp)
            except Exception:
                pass
    except Exception:
        pass


def ensure_node():
    if os.path.isfile(NODE_BIN):
        try:
            r = subprocess.run(
                [NODE_BIN, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if r.returncode == 0 and r.stdout.strip().startswith("v"):
                print(f"[Beastlink] Node: {r.stdout.strip()}")
                return NODE_BIN
        except Exception:
            pass

    try:
        os.remove(NODE_BIN)
    except Exception:
        pass

    print("[Beastlink] Installing Node.js...")
    try:
        subprocess.run(
            [
                sys.executable, "-m", "pip", "install",
                "--no-cache-dir", "nodejs-wheel-binaries",
            ],
            check=False,
            timeout=180,
        )
    except Exception as e:
        print(f"[Beastlink] Node install failed: {e}")
        return None

    for root, dirs, files in os.walk("/home/container/.local"):
        if "node" in files:
            src = os.path.join(root, "node")
            if os.access(src, os.X_OK):
                try:
                    os.makedirs("/home/container/bin", exist_ok=True)
                    shutil.copy2(src, NODE_BIN)
                    os.chmod(NODE_BIN, 0o755)
                    return NODE_BIN
                except Exception:
                    pass
    return None


def run_autofix():
    cleanup_disk()
    try:
        stat = shutil.disk_usage("/home/container")
        free_mb = stat.free / (1024 * 1024)
        print(f"[Beastlink] Free disk: {free_mb:.0f} MB")
    except Exception:
        pass
    return ensure_node()