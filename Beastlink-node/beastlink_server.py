#!/usr/bin/env python3
"""
Beastlink Audio Node Launcher.

A pure-Python, Lavalink-compatible audio node. No Java required.

Usage:
    python beastlink_server.py
    python beastlink_server.py --port 2444 --password secret
    python beastlink_server.py --generate-config

Author: VampireDev
Repository: https://github.com/vampirejjjadev/beastlink
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

VERSION = "0.2.2"
ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "beastlink.yml"

if os.name == "nt":
    os.system("")

ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "gray": "\033[90m",
    "white": "\033[97m",
}


def paint(text: str, *styles: str) -> str:
    prefix = "".join(ANSI.get(s, "") for s in styles)
    return f"{prefix}{text}{ANSI['reset']}"


BANNER = r"""
   ____                 _   _ _       _
  | __ )  ___  __ _ ___| |_| (_)_ __ | | __
  |  _ \ / _ \/ _` / __| __| | | '_ \| |/ /
  | |_) |  __/ (_| \__ \ |_| | | | | |   <
  |____/ \___|\__,_|___/\__|_|_|_| |_|_|\_\
"""

DEFAULT_YML = """\
# Beastlink Node Configuration
# Drop-in equivalent of Lavalink's application.yml

server:
  host: "0.0.0.0"
  port: 2333
  password: "youshallnotpass"

cookies:
  path: "cookies/cookies.txt"
  from_browser: ""

ytdlp:
  js_runtime: "node"
  extra_args: ""

logging:
  level: "INFO"
  file: "logs/beastlink.log"

audio:
  buffer_size: 1048576
  sample_rate: 48000
  channels: 2
"""

PLUGINS_README = """\
Beastlink Plugins Folder.

Drop any .py file here and it will auto-load on startup.

Simple plugin (function style):

    def setup(node):
        node.on("track_start", lambda t: print(t.title))

Full plugin (class style):

    from beastlink.plugins import Plugin

    class MyPlugin(Plugin):
        name = "my_plugin"
        version = "1.0.0"

        def on_load(self, node):
            print("ready")

        def on_track_start(self, node, track):
            print(f"playing: {track.title}")

Available hooks:

    on_load(node)
    on_unload(node)
    on_track_start(node, track)
    on_track_end(node, track)
    on_track_exception(node, track, error)
    register_filters() -> dict

Files starting with "_" are ignored. A bad plugin will not crash the node.
"""

EXAMPLE_PLUGIN = '''\
from beastlink.plugins import Plugin


class ExampleLyrics(Plugin):
    name = "example_lyrics"
    version = "1.0.0"

    def on_load(self, node):
        print("  -> example_lyrics ready")

    def on_track_start(self, node, track):
        print(f"  ~ now playing: {track.title}")
'''

COOKIES_README = """\
Beastlink Cookies Folder.

Drop a "cookies.txt" file in this folder to authenticate YouTube
requests. Without cookies, YouTube may block the node with:
    "Sign in to confirm you're not a bot"

When to use cookies:

    - YouTube returns "Sign in to confirm you're not a bot"
    - Tracks fail to load but other sources work
    - Running on a VPS or datacenter IP (most common case)

How to obtain cookies.txt:

    1. Install the "Get cookies.txt LOCALLY" browser extension
       for Chrome, Brave, Edge, or Firefox.
    2. Log into YouTube in that browser (use a throwaway account).
    3. Click the extension icon and export in Netscape format.
    4. Save the file as cookies/cookies.txt.
    5. Restart the Beastlink node.

Alternative: auto-pull from a local browser.

    Edit beastlink.yml:

        cookies:
          path: ""
          from_browser: "chrome"

    On Windows, the browser must be closed or the cookie DB is locked.

Troubleshooting:

    - Cookies expire every 1-2 weeks. Re-export periodically.
    - Never share cookies.txt. It grants full account access.
    - Never commit cookies.txt to GitHub. It is already gitignored.
"""


def info(message: str, color: str = "white") -> None:
    tag = paint("[Beastlink]", "bold", "magenta")
    print(f"  {tag} {paint(message, color)}", flush=True)


def status_row(label: str, value: str, ok: bool = True) -> None:
    dot = paint("\u25cf", "green" if ok else "yellow")
    lbl = paint(f"{label:<22}", "gray")
    val = paint(value, "white")
    print(f"  {dot}  {lbl} {val}")


def pip_install(*packages: str) -> None:
    info(f"Installing: {' '.join(packages)}", "yellow")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", *packages]
        )
    except subprocess.CalledProcessError as exc:
        info(f"pip install failed: {exc}", "red")
        sys.exit(1)


def ensure_pyyaml() -> None:
    try:
        import yaml  # noqa: F401
    except ImportError:
        pip_install("pyyaml")


def ensure_beastlink() -> None:
    try:
        import beastlink  # noqa: F401
    except ImportError:
        info("beastlink package not found, installing from PyPI", "yellow")
        pip_install("beastlink")


def scaffold() -> bool:
    """Create folders and default files. Returns True on first run."""
    first_run = not CONFIG_FILE.exists()

    for folder in ("plugins", "cookies", "logs"):
        (ROOT / folder).mkdir(exist_ok=True)

    templates = {
        "beastlink.yml": DEFAULT_YML,
        "plugins/README.txt": PLUGINS_README,
        "plugins/example_lyrics.py": EXAMPLE_PLUGIN,
        "cookies/README.txt": COOKIES_README,
    }
    for rel_path, content in templates.items():
        target = ROOT / rel_path
        if not target.exists():
            target.write_text(content, encoding="utf-8")

    return first_run


def load_config(path: Path) -> dict:
    import yaml

    if not path.exists():
        path.write_text(DEFAULT_YML, encoding="utf-8")

    with path.open("r", encoding="utf-8") as handle:
        user_config = yaml.safe_load(handle) or {}

    defaults = yaml.safe_load(DEFAULT_YML)
    for section, values in defaults.items():
        if section not in user_config:
            user_config[section] = values
        elif isinstance(values, dict):
            for key, default in values.items():
                user_config[section].setdefault(key, default)

    return user_config


def export_env(
    config: dict,
    host_override: str | None = None,
    port_override: int | None = None,
    password_override: str | None = None,
) -> dict:
    server = config.get("server", {})
    cookies = config.get("cookies", {})
    ytdlp = config.get("ytdlp", {})
    logging_cfg = config.get("logging", {})
    audio = config.get("audio", {})

    host = host_override or server.get("host", "0.0.0.0")
    port = port_override or int(server.get("port", 2333))
    password = password_override or server.get("password", "youshallnotpass")

    cookie_path = cookies.get("path") or ""
    if cookie_path and not Path(cookie_path).is_absolute():
        cookie_path = str((ROOT / cookie_path).resolve())

    log_file = logging_cfg.get("file") or ""
    if log_file and not Path(log_file).is_absolute():
        log_file = str((ROOT / log_file).resolve())

    mapping = {
        "BEASTLINK_HOST": str(host),
        "BEASTLINK_PORT": str(port),
        "BEASTLINK_PASSWORD": str(password),
        "BEASTLINK_COOKIES": cookie_path,
        "BEASTLINK_COOKIES_BROWSER": str(cookies.get("from_browser", "") or ""),
        "BEASTLINK_JS_RUNTIME": str(ytdlp.get("js_runtime", "node") or ""),
        "BEASTLINK_YTDLP_ARGS": str(ytdlp.get("extra_args", "") or ""),
        "BEASTLINK_LOG_LEVEL": str(logging_cfg.get("level", "INFO")),
        "BEASTLINK_LOG_FILE": log_file,
        "BEASTLINK_BUFFER_SIZE": str(audio.get("buffer_size", 1048576)),
        "BEASTLINK_SAMPLE_RATE": str(audio.get("sample_rate", 48000)),
        "BEASTLINK_CHANNELS": str(audio.get("channels", 2)),
    }

    for key, value in mapping.items():
        os.environ[key] = value

    return mapping


def detect_node() -> str:
    try:
        output = subprocess.check_output(
            ["node", "--version"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return output or "unknown"
    except Exception:
        return "auto-install pending"


def detect_ffmpeg() -> bool:
    try:
        subprocess.check_output(
            ["ffmpeg", "-version"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def print_report(
    config: dict,
    env: dict,
    first_run: bool,
    plugins: list[str] | None = None,
) -> None:
    print(paint(BANNER, "magenta", "bold"))
    print(paint(f"  Beastlink Audio Node  \u00b7  v{VERSION}", "cyan", "bold"))
    print(paint("  Pure Python  \u00b7  No Java  \u00b7  No Lavalink", "gray"))
    print(paint("  https://github.com/vampirejjjadev/beastlink", "gray"))
    print()

    print(paint("  \u2500\u2500 Environment \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", "gray"))
    status_row("Python", f"{platform.python_version()} ({platform.system()})")

    node_version = detect_node()
    status_row("Node.js", node_version, ok=node_version != "auto-install pending")

    ffmpeg_ok = detect_ffmpeg()
    status_row("FFmpeg", "detected" if ffmpeg_ok else "MISSING", ok=ffmpeg_ok)
    print()

    if first_run:
        print(paint("  \u2500\u2500 First-run setup \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", "yellow"))
        status_row("beastlink.yml", "created")
        status_row("plugins/", "created")
        status_row("cookies/", "created")
        status_row("logs/", "created")
        print()

    print(paint("  \u2500\u2500 Configuration \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", "gray"))
    status_row("Host", f"{env['BEASTLINK_HOST']}:{env['BEASTLINK_PORT']}")
    status_row("Password", "\u2022" * min(len(env["BEASTLINK_PASSWORD"]), 16))

    cookie_path = env["BEASTLINK_COOKIES"]
    cookies_ok = bool(cookie_path) and Path(cookie_path).exists()
    status_row(
        "Cookies",
        cookie_path if cookies_ok else "(disabled)",
        ok=cookies_ok,
    )

    if cookies_ok:
        age_days = (time.time() - Path(cookie_path).stat().st_mtime) / 86400
        if age_days > 14:
            warning = paint(
                f"     !  Cookies are {int(age_days)} days old, re-export them",
                "yellow",
            )
            print(warning)

    status_row("JS Runtime", env["BEASTLINK_JS_RUNTIME"] or "auto")
    status_row("Log Level", env["BEASTLINK_LOG_LEVEL"])
    print()

    if plugins:
        print(paint(
            f"  \u2500\u2500 Plugins ({len(plugins)}) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500",
            "gray",
        ))
        for name in plugins:
            status_row(name, "loaded")
    else:
        print(paint("  \u2500\u2500 Plugins (0) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", "gray"))
        print(paint("     Drop .py files into ./plugins/ to extend", "dim"))
    print()

    print(paint("  \u2500\u2500 Node \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500", "gray"))
    status_row("Started", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print(paint("  Beastlink is ready. Waiting for connections...", "green", "bold"))
    print(paint("    Press Ctrl+C to stop.", "dim"))
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="beastlink-server",
        description="Beastlink Audio Node: Lavalink-compatible, pure Python.",
    )
    parser.add_argument("--config", "-c", default=str(CONFIG_FILE),
                        help="Path to beastlink.yml")
    parser.add_argument("--host", help="Override bind host")
    parser.add_argument("--port", "-p", type=int, help="Override port")
    parser.add_argument("--password", "--pass", dest="password",
                        help="Override password")
    parser.add_argument("--generate-config", action="store_true",
                        help="Write default beastlink.yml and exit")
    parser.add_argument("--no-bootstrap", action="store_true",
                        help="Skip auto-install of dependencies")
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()

    if args.generate_config:
        scaffold()
        print(paint(f"  Config written: {config_path}", "green"))
        return 0

    if not args.no_bootstrap:
        ensure_pyyaml()
        ensure_beastlink()

    first_run = scaffold()
    config = load_config(config_path)
    env = export_env(
        config,
        host_override=args.host,
        port_override=args.port,
        password_override=args.password,
    )

    plugin_names: list[str] = []
    try:
        from beastlink.plugins import load_plugins  # type: ignore
        loaded = load_plugins(ROOT / "plugins", node=None) or []
        plugin_names = [getattr(plugin, "name", "unnamed") for plugin in loaded]
    except Exception:
        plugin_names = []

    print_report(config, env, first_run=first_run, plugins=plugin_names)

    try:
        from beastlink.server import main as server_main  # type: ignore
    except ImportError as exc:
        info(f"Could not import beastlink.server: {exc}", "red")
        info("Try: pip install --upgrade beastlink", "yellow")
        return 1

    try:
        result = server_main()
        return int(result) if isinstance(result, int) else 0
    except KeyboardInterrupt:
        print()
        info("Shutting down", "yellow")
        return 0
    except Exception as exc:
        info(f"Server crashed: {exc}", "red")
        return 1


if __name__ == "__main__":
    sys.exit(main())