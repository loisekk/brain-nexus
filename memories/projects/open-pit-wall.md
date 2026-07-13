# Open Pit Wall

**Last updated:** 2026-06-24

## Overview
F1 telemetry WebSocket broadcaster for testing dashboards. Python package with CLI, data loader, and WebSocket server layers.

## Architecture
- **CLI menu** (`cli_menu.py`): Interactive season/weekend/session picker using questionary + rich
- **Data loader** (`data_loader.py`): FastF1-backed download pipeline, JSON cache, resampling, safety car position simulation
- **Telemetry broadcaster** (`telemetry_broadcaster.py`): Async WebSocket server with channel-based subscriptions (telemetry.drivers, leaderboard, race_control, telemetry.weather, telemetry.lap, per-driver channels)
- **Lib** (`lib/`): season, time parsing, tyre compound mapping helpers

## Key decisions
- Replay cache stored as JSON (not pickle) — avoids unsafe deserialization
- Multiprocessing for parallel driver telemetry processing
- Safety car positions simulated (F1 API doesn't provide SC GPS)
- Sorted imports, no comments in code style

## Key files
- `open_pit_wall/data_loader.py` ~1400 lines — core data pipeline
- `open_pit_wall/telemetry_broadcaster.py` ~1175 lines — WebSocket server
- `open_pit_wall/cli_menu.py` ~333 lines — interactive UI
- `open_pit_wall/main.py` — entry point dispatching to replay or menu

## Config
- `opencode.json` — AI assistant config
- `pyrightconfig.json` — type checker (relaxed: reportMissingImports false, etc.)
- `pyproject.toml` — build system, dependencies, CLI entry point

## Dependencies
fastf1, pandas, numpy, websockets, scipy, questionary, rich, matplotlib

## Tests
pytest tests in `tests/` covering: broadcaster, data loader, CLI interrupts, main entry point, driver telemetry trace example

## Remote
`origin` = `https://github.com/loisekk/open-pit-wall.git` (branch: main)
