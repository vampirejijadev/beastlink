<div align="center">

# Beastlink

**A self-contained music plugin for Discord bots — available for Python and JavaScript.**

Play music from YouTube, YouTube Music, Spotify, SoundCloud, Apple Music, and Deezer.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Node](https://img.shields.io/badge/node-18%2B-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-beastlink-orange.svg)](https://pypi.org/project/beastlink/)
[![npm](https://img.shields.io/badge/npm-beastlink-red.svg)](https://www.npmjs.com/package/beastlink)

</div>

---

## Table of Contents

- [About](#about)
- [Languages](#languages)
- [Features](#features)
- [Supported Sources](#supported-sources)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Project Structure](#project-structure)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## About

Beastlink is a music plugin for Discord bots. It is designed to be simple, fast, and self-contained. No external server. No Java. No complicated setup.

You install it with one command. You add a few lines to your bot. It works.

---

## Languages

Beastlink is available for both Python and JavaScript.

| Language   | Package    | Install command           |
|------------|------------|---------------------------|
| Python     | `beastlink`| `pip install beastlink`   |
| JavaScript | `beastlink`| `npm install beastlink`   |

Each language has its own source folder inside this repository:

- `/python` — Python version
- `/javascript` — JavaScript version

---

## Features

- **Self-contained** — no external server required
- **One-command install**
- **Multi-source playback** — six supported platforms
- **Simple API** — play, pause, resume, skip, stop, volume, loop, queue
- **Queue system** — add, remove, clear, shuffle, peek
- **Lightweight** — fast startup, low memory usage
- **MIT licensed**

---

## Supported Sources

| Source          | Status     |
|-----------------|------------|
| YouTube         | Supported  |
| YouTube Music   | Supported  |
| Spotify         | Supported  |
| SoundCloud      | Supported  |
| Apple Music     | Supported  |
| Deezer          | Supported  |

---

## Requirements

- **Python 3.9+** or **Node.js 18+**
- **ffmpeg** installed on the machine running your bot
- **PyNaCl** (Python) or **@discordjs/opus** (JavaScript) for voice support

---

## Installation

### Python

```bash
pip install beastlink