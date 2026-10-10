"""
Beastlink ASCII banner + startup printer.
Author: VampireDev
"""
from __future__ import annotations
import os
import platform
import sys
from datetime import datetime

# Enable ANSI on Windows
if os.name == "nt":
    os.system("")

C = {
    "reset":   "\033[0m",
    "bold":    "\033[1m",
    "dim":     "\033[2m",
    "red":     "\033[91m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "blue":    "\033[94m",
    "magenta": "\033[95m",
    "cyan":    "\033[96m",
    "white":   "\033[97m",
    "gray":    "\033[90m",
}

BEASTLINK_ART = r"""
   ____                 _   _ _       _
  | __ )  ___  __ _ ___| |_| (_)_ __ | | __
  |  _ \ / _ \/ _` / __| __| | | '_ \| |/ /
  | |_) |  __/ (_| \__ \ |_| | | | | |   <
  |____/ \___|\__,_|___/\__|_|_|_| |_|_|\_\
"""


def _c(text: str, *colors: str) -> str:
    return "".join(C[c] for c in colors) + text + C["reset"]


def print_banner(version: str = "0.2.2") -> None:
    art = _c(BEASTLINK_ART, "magenta", "bold")
    print(art)
    print(_c(f"  Beastlink Audio Node  ·  v{version}", "cyan", "bold"))
    print(_c("  Pure Python  ·  No Java  ·  No Lavalink", "gray"))
    print(_c("  https://github.com/vampirejjjadev/beastlink", "gray"))
    print()


def _row(label: str, value: str, ok: bool = True) -> None:
    dot = _c("●", "green" if ok else "yellow")
    lbl = _c(f"{label:<22}", "gray")
    val = _c(value, "white")
    print(f"  {dot}  {lbl} {val}")


def print_startup_report(cfg: dict, first_run: bool = False,
                          plugins: list | None = None,
                          node_version: str = "auto") -> None:
    srv = cfg.get("server", {})
    ytd = cfg.get("ytdlp", {})
    cook = cfg.get("cookies", {})

    print(_c("  ── Environment ─────────────────────────────────", "gray"))
    _row("Python", f"{platform.python_version()} ({platform.system()})")
    _row("Node.js", node_version)
    _row("FFmpeg", "detected")
    print()

    if first_run:
        print(_c("  ── First-run setup ─────────────────────────────", "yellow"))
        _row("beastlink.yml", "created", ok=True)
        _row("plugins/", "created", ok=True)
        _row("cookies/", "created", ok=True)
        _row("logs/", "created", ok=True)
        print()

    print(_c("  ── Configuration ───────────────────────────────", "gray"))
    _row("Host", f"{srv.get('host','0.0.0.0')}:{srv.get('port',2333)}")
    _row("Password", "•" * min(len(str(srv.get('password',''))), 16))
    _row("JS Runtime", ytd.get("js_runtime", "node") or "auto")
    _row("Cookies", cook.get("path", "") or "(disabled)",
         ok=bool(cook.get("path")))
    print()

    if plugins:
        print(_c(f"  ── Plugins ({len(plugins)}) ─────────────────────────────", "gray"))
        for name in plugins:
            _row(name, "loaded")
        print()
    else:
        print(_c("  ── Plugins (0) ─────────────────────────────────", "gray"))
        print(_c("     Drop .py files into ./plugins/ to extend.", "dim"))
        print()

    print(_c("  ── Node ────────────────────────────────────────", "gray"))
    _row("Started", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    print(_c("  ✔ Beastlink is ready. Waiting for connections...", "green", "bold"))
    print(_c("    Press Ctrl+C to stop.", "dim"))
    print()