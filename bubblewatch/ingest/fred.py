from __future__ import annotations

from datetime import datetime, timezone
from io import StringIO

import pandas as pd

from .. import config, storage


def _fetch_series(series_id: str, start_date: str = config.FRED_START) -> pd.DataFrame:
    import shutil
    import subprocess
    import urllib.request
    from io import StringIO

    url = (
        "https://fred.stlouisfed.org/graph/fredgraph.csv"
        f"?id={series_id}&cosd={start_date}"
    )
    text = None
    if shutil.which("curl"):
        try:
            res = subprocess.run(
                ["curl", "-s", "-f", "-m", "15", url],
                capture_output=True,
                text=True,
                timeout=18,
            )
            if res.returncode == 0 and res.stdout.strip():
                text = res.stdout
        except Exception:
            text = None

    if text is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            text = resp.read().decode("utf-8")

    df = pd.read_csv(StringIO(text))
    cols = list(df.columns)
    date_col = cols[0]
    value_col = [c for c in cols if c != date_col][0]
    df = df.rename(columns={date_col: "date", value_col: "value"})
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    return df


def run() -> int:
    today = datetime.now(timezone.utc).strftime(config.RUN_DATE_FMT)
    existing = storage.read_table("fred_daily")
    frames = []

    for key, series_id in config.FRED_SERIES.items():
        # Incremental fetch: look back 14 days from latest date in lake to keep queries fast and avoid FRED timeouts
        start_date = config.FRED_START
        if existing is not None and not existing.empty:
            series_rows = existing[existing["series"] == key]
            if not series_rows.empty:
                max_d = pd.Timestamp(series_rows["date"].max())
                start_date = (max_d - pd.Timedelta(days=14)).strftime(config.RUN_DATE_FMT)

        try:
            sub = _fetch_series(series_id, start_date=start_date)
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
