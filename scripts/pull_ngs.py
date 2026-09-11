"""
Pulls Next Gen Stats (passing, rushing, receiving) for the Green Bay Packers
from the nflverse-data project and writes them to /data as JSON for the
dashboard to consume.

Source: https://github.com/nflverse/nflverse-data (via the nflreadpy package)
NGS data has been available since the 2016 season.

Usage:
    python scripts/pull_ngs.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import nflreadpy as nfl
import polars as pl

TEAM = "GB"
STAT_TYPES = ["passing", "rushing", "receiving"]
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def pull_stat_type(stat_type: str) -> pl.DataFrame:
    """Load full NGS history for a stat type and filter to one team."""
    df = nfl.load_nextgen_stats(seasons=True, stat_type=stat_type)
    return df.filter(pl.col("team_abbr") == TEAM).sort(["season", "week"])


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    manifest = {
        "team": TEAM,
        "last_updated_utc": datetime.now(timezone.utc).isoformat(),
        "stat_types": {},
    }

    for stat_type in STAT_TYPES:
        df = pull_stat_type(stat_type)
        records = df.to_dicts()

        out_path = DATA_DIR / f"ngs_{stat_type}.json"
        out_path.write_text(json.dumps(records, indent=None, default=str))

        seasons = sorted({r["season"] for r in records})
        manifest["stat_types"][stat_type] = {
            "row_count": len(records),
            "seasons": seasons,
            "file": out_path.name,
        }
        print(f"{stat_type}: {len(records)} rows -> {out_path}")

    (DATA_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("Wrote manifest.json")


if __name__ == "__main__":
    main()
