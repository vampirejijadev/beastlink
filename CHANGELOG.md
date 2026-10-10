# Changelog

All notable changes to Beastlink will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.2] - 2026-10-10

### Added
- Plugin system with `Plugin` base class and `load_plugins()` loader
- Standalone launcher `beastlink_server.py` with ASCII banner
- Auto-scaffold on first run: creates `beastlink.yml`, `plugins/`, `cookies/`, `logs/`
- Professional startup report with color-coded status indicators
- Cookie freshness warning for cookies older than 14 days
- `beastlink-node/` standalone template folder
- `beastlink.yml.example` config template
- Dockerfile for containerized deployment
- GitHub Actions workflow for auto-publish to PyPI
- Issue templates for bug reports
- Security policy

### Changed
- Renamed `server_clinet.py` to `server_client.py` (typo fix)
- Improved console output formatting

### Fixed
- Import path corrections after rename
- Cleaned up build artifacts

## [0.2.1] - 2026-09-15

### Added
- Multi-bot server mode
- Remote server mode (bot on Host A, node on Host B)
- URL and password authentication
- Auto Node.js install on first run
- Auto disk cleanup on restart

### Fixed
- Prefetch buffer memory leak
- Volume control edge cases

## [0.2.0] - 2026-08-20

### Added
- Audio filters (bassboost, treble, 8d, nightcore, vaporwave, karaoke, lofi, pop, rock, electronic, soft, concert, stadium)
- Autoplay feature
- Playlist support
- Search cache

### Changed
- Switched from download mode to PIPE streaming

## [0.1.0] - 2026-07-01

### Added
- Initial release
- PIPE streaming via yt-dlp + ffmpeg
- Play, pause, resume, skip, stop, queue
- YouTube, Spotify, SoundCloud, Apple Music, Deezer, Twitch, Bandcamp support
- 6 language clients (JavaScript, Java, C#, Go, Rust, PHP)
