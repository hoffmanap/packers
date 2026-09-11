# packers

Player tracking data for the Green Bay Packers, pulled weekly from NFL Next Gen
Stats and rendered as an interactive dashboard.

## Data source

Data comes from the [nflverse-data](https://github.com/nflverse/nflverse-data)
project via the [nflreadpy](https://github.com/nflverse/nflreadpy) Python
package, rather than scraping nextgenstats.nfl.com directly. nflverse already
scrapes and republishes NGS data on an automated schedule, structured as clean
tables — this pipeline just pulls that, filters to GB, and re-publishes it in
a shape the dashboard can use.

Three stat types, each at the player-week level:

- **passing** — avg time to throw, air yards (completed/intended), aggressiveness,
  completion % above expectation, etc.
- **rushing** — efficiency, time to line of scrimmage, rush yards over expected,
  % of attempts vs. 8+ man boxes
- **receiving** — avg separation, cushion, YAC above expectation, % share of
  intended air yards

NGS data is available from the 2016 season onward. Note there's typically a
lag of several hours to a day between a game airing and nflverse's own
pipeline refreshing, so this is built for weekly recap use, not live tracking.

## Pipeline

`scripts/pull_ngs.py` pulls full history each run (not just the latest week),
filters to `team_abbr == "GB"`, and writes:

- `data/ngs_passing.json`
- `data/ngs_rushing.json`
- `data/ngs_receiving.json`
- `data/manifest.json` — row counts, season coverage, and last-updated timestamp

Pulling full history each time (rather than incrementally appending) keeps
the script simple and self-correcting — if nflverse revises a past week's
numbers, we pick that up automatically.

### Automation

`.github/workflows/update_data.yml` runs the script every Tuesday at 13:00 UTC
(after Monday Night Football) via GitHub Actions, and commits the refreshed
JSON back to the repo if anything changed. It can also be triggered manually
from the Actions tab.

## Running locally

```bash
pip install -r requirements.txt
python scripts/pull_ngs.py
```

## Status

- [x] Data source identified and pipeline script written
- [x] Weekly automation configured (GitHub Actions)
- [ ] Interactive dashboard (in progress)
