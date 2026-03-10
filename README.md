# Who Up? New Mexico Edition

A live, automated dashboard showing what ~665,000 New Mexicans are doing right now — working, traveling, eating, or at leisure — visualized as a grid of colored squares (1 square = 1,000 people).

## Data Sources

| Source | What it provides |
|---|---|
| ABQ Sunport FIDS (Infax portal) | Live flight count → traveler estimate |
| City of Albuquerque Open Data (`data.cabq.gov`) | Active transit station reports → commuter estimate |
| U.S. Census Bureau | ABQ + Rio Rancho combined population (~665,000) |

Work/leisure percentages shift automatically based on **time of day** (Mountain Time).

## How to Run

### 1. Install dependencies
```bash
pip install "scrapling[fetchers]"
scrapling install
```

### 2. Start the live update loop
```bash
python run_pulse.py
```
This runs all three engines, writes `city_pulse.json`, and refreshes every 5 minutes automatically.

### 3. View the dashboard
In a **separate terminal**, serve the folder:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser. The page auto-refreshes its data every 5 minutes.

> ⚠️ **You cannot open index.html directly as a file (file://)** — the browser will block the `fetch()` call to city_pulse.json. You must use the local server above.

## File Overview

| File | Purpose |
|---|---|
| `engine.py` | Scrapes ABQ Sunport for active flights |
| `transit_pulse.py` | Scrapes CABQ open data for transit activity |
| `generate_nm_grid.py` | Combines data, applies time-of-day logic, writes grid values |
| `run_pulse.py` | Orchestrates all three engines in a live loop |
| `city_pulse.json` | Shared data file read by the dashboard |
| `index.html` | Visual grid dashboard |
