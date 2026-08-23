from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from .. import config, storage


def run() -> int:
    today = datetime.now(timezone.utc).strftime(config.RUN_DATE_FMT)
    path = config.CAPEX_MANUAL_CSV
    if not path.exists():
        storage.log_run("capex", "skipped", detail=f"no manual file at {path.name}")
        return 0
    try:
        df = pd.read_csv(path)
        df["period"] = df["period"].astype(str).str.strip()
        for col in ["hyperscaler_capex_usd_b", "nvda_rev_yoy_pct"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["hyperscaler_capex_usd_b", "nvda_rev_yoy_pct"], how="all")
    except Exception as exc:
        storage.log_run("capex", "error", detail=str(exc)[:200])
        return 0
    if df.empty:
        storage.log_run("capex", "skipped", detail="manual file has no data rows")
        return 0

    df = df[["period", "hyperscaler_capex_usd_b", "nvda_rev_yoy_pct"]]
    df["ingested_at"] = today
    total = storage.write_table(df, "capex_quarterly", ["period"])
    storage.log_run("capex", "ok", rows=len(df),
                    detail=f"total={total} latest_period={df['period'].max()}")
    return len(df)


if __name__ == "__main__":
    run()
