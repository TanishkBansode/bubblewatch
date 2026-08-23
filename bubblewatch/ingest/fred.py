from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO

import pandas as pd

from .. import config, storage


def _fetch_series(series_id: str) -> pd.DataFrame:
    import requests

    url = (
        "https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}&cosd={config.FRED_START}"
    )
    resp = requests.get(url, timeout=30, headers={"User-Agent": "bubblewatch/0.1"})
    resp.raise_for_status()
    df = pd.read_csv(StringIO(resp.text))
    cols = list(df.columns)
    date_col = cols[0]
    value_col = [c for c in cols if c != date_col][0]
    df = df.rename(columns={date_col: "date", value_col: "value"})
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    return df


def run() -> int:
    today = datetime.now(timezone.utc).strftime(config.RUN_DATE_FMT)
    frames = []
    for key, series_id in config.FRED_SERIES.items():
        try:
            sub = _fetch_series(series_id)
        except Exception as exc:
            storage.log_run("fred", "error", detail=f"{series_id}: {exc}")
            continue
        if sub.empty:
            continue
        sub = sub.copy()
        sub["series"] = key
        frames.append(sub)

    if not frames:
        lake = storage.read_table("fred_daily")
        status = "failed" if lake is None or lake.empty else "ok_stale"
        storage.log_run("fred", status, detail="no fresh pulls succeeded")
        return 0

    data = pd.concat(frames, ignore_index=True)
    data["source"] = "fred"
    data["ingested_at"] = today
    total = storage.write_table(data, "fred_daily", ["series", "date"])
    latest = data.groupby("series")["date"].max().to_dict()
    storage.log_run("fred", "ok", rows=len(data),
                    detail=f"total={total} latest={latest}")
    return len(latest)


if __name__ == "__main__":
    run()
