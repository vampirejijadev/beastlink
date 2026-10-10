<div align="center">

# Beastlink

**A self-contained music plugin for Python Discord bots.**

Stream music from YouTube, Spotify, SoundCloud, Apple Music, Deezer, and 1000+ sites.

[![PyPI](https://img.shields.io/pypi/v/beastlink.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/beastlink/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![Downloads](https://img.shields.io/badge/downloads-0-brightgreen.svg?style=flat-square)](https://pypi.org/project/beastlink/)

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Server Mode](#server-mode) • [Multi-Language](#multi-language-clients) • [FAQ](#faq)

</div>

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Supported Sources](#supported-sources)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Standalone Mode](#standalone-mode)
  - [Same-Host Server Mode](#same-host-server-mode)
  - [Remote Server Mode](#remote-server-mode)
- [Configuration](#configuration)
- [Commands](#commands)
- [Filters](#filters)
- [Multi-Language Clients](#multi-language-clients)
- [Server API](#server-api)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## About

Beastlink is a **self-contained music plugin** for Python Discord bots. It uses **yt-dlp + ffmpeg** to stream audio directly to Discord — **no download needed, no external Java server, no complex setup**.

Just install, add a few lines to your bot, and music works.

Beastlink supports **three operation modes**:

- **Standalone** — Everything runs inside your bot (simplest)
- **Same-Host Server** — Server and bot on the same machine (share with friends)
- **Remote Server** — Server on a VPS, bot anywhere (like Lavalink)

---

## Features

| Feature | Description |
|---------|-------------|
| **PIPE Streaming** | yt-dlp → ffmpeg pipe — no download, no 403 errors |
| **Prefetch** | Next song resolves in background — plays instantly |
| **Auto Node.js** | Installs Node.js on first run — no manual setup |
| **Auto Cleanup** | Frees disk space every restart |
| **Multi-Source** | YouTube, Spotify, SoundCloud, Apple Music, Deezer, Twitch, Bandcamp |
| **Filters** | Bass, treble, 8d, nightcore, vaporwave, karaoke, lofi, pop, rock, concert, stadium |
| **Queue System** | Add, remove, shuffle, loop, clear |
| **Autoplay** | Auto-plays similar songs when queue ends |
| **Playlists** | Full playlist URL support |
| **Search** | `/search <query>` returns top 5 results |
| **Multi-Bot Server** | One server, unlimited bots |
| **Remote Client** | Bot on one host, server on another |
| **7 Languages** | Python, JavaScript, Java, C#, Go, Rust, PHP |
| **Free Forever** | MIT licensed, no paid tier |

---

## Supported Sources

| Source | Status | Notes |
|--------|:---:|-------|
| YouTube | ✅ Full | Direct stream via yt-dlp |
| YouTube Music | ✅ Full | Detected automatically |
| Spotify | ✅ Full | Metadata → YouTube match |
| SoundCloud | ✅ Full | Direct stream |
| Apple Music | ✅ Full | Metadata → YouTube match |
| Deezer | ✅ Full | Metadata → YouTube match |
| Twitch | ✅ Full | Live streams + VODs |
| Bandcamp | ✅ Full | Direct stream |
| 1000+ sites | ✅ Full | via yt-dlp extractors |

---

## Requirements

- **Python 3.9+**
- **ffmpeg** installed on the host
- **Node.js** — *auto-installed on first run*

### Install ffmpeg

| Platform | Command |
|----------|---------|
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Alpine | `sudo apk add ffmpeg` |
| macOS | `brew install ffmpeg` |
| Windows | [Download from ffmpeg.org](https://ffmpeg.org/download.html) |

---

## Installation

```bash
pip install beastlink