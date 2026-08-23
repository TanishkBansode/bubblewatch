from __future__ import annotations

import json

import numpy as np
import pandas as pd

from . import config, storage
from .features import MODEL_FEATURES, basket_index, build_feature_frame, market_closes

HORIZON_DAYS = 5


def _ai_index(closes: pd.DataFrame) -> pd.Series:
    rets = closes.pct_change()
    return basket_index(rets, config.AI_COMPLEX)


def make_supervised(feats: pd.DataFrame, idx: pd.Series) -> pd.DataFrame:
    df = feats.copy()
    df["target_up"] = (idx.shift(-HORIZON_DAYS) / idx - 1.0 > 0).astype(float)
    df = df.dropna(subset=[c for c in MODEL_FEATURES if c in df.columns])
    df = df.dropna(subset=["target_up"])
    return df


def train_direction_model() -> dict:
    market = storage.read_table("market_prices")
    fred = storage.read_table("fred_daily")
    if market is None or market.empty:
        return {"status": "no_data"}
    closes = market_closes(market)
    idx = _ai_index(closes)
    feats = build_feature_frame(market, fred).dropna(how="all")
    data = make_supervised(feats, idx)
    if len(data) < 120:
        return {"status": "insufficient_history", "rows": len(data)}

    split = int(len(data) * 0.8)
    X_cols = [c for c in MODEL_FEATURES if c in data.columns]
    X_train, y_train = data[X_cols].iloc[:split], data["target_up"].iloc[:split]
    X_test, y_test = data[X_cols].iloc[split:], data["target_up"].iloc[split:]

    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    model = make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=1000))
    model.fit(X_train, y_train)

    result = {"status": "ok", "train_rows": int(split), "test_rows": int(len(y_test))}
    if len(y_test) > 20:
        proba = model.predict_proba(X_test)[:, 1]
        brier = float(np.mean((proba - y_test.to_numpy()) ** 2))
        acc = float(((proba > 0.5).astype(float) == y_test.to_numpy()).mean())
        base = float(max(y_test.mean(), 1 - y_test.mean()))
        result.update({"brier": round(brier, 4),
                       "accuracy": round(acc, 3),
                       "majority_baseline_acc": round(base, 3)})
    latest = data[X_cols].iloc[[-1]]
    p_up = float(model.predict_proba(latest)[0, 1])
    result["p_ai_up_5d"] = round(p_up, 3)
    result["asof"] = str(data.index[-1].date())
    return result


def direction_predictions(proxy: dict) -> list[dict]:
    p = proxy.get("p_ai_up_5d") if proxy.get("status") == "ok" else None
    return [
        {
            "target": "AI_complex_dir_5d",
            "horizon_days": HORIZON_DAYS,
            "p_model": p,
            "p_constant": 0.5,
            "note": "logistic on equity+credit features; scored vs constant baseline",
        }
    ]


def append_run_to_ledger(snap: dict, regime: tuple[str, str], proxy: dict,
                         preds: list[dict]) -> None:
    from .storage import append_ledger, features_hash

    record = {
        "ts": pd.Timestamp.utcnow().isoformat(timespec="seconds"),
        "run_date": pd.Timestamp.utcnow().strftime(config.RUN_DATE_FMT),
        "model_version": config.MODEL_VERSION,
        "features_hash": features_hash({k: v for k, v in snap.items()}),
        "regime": regime[0],
        "temperature": snap.get("temperature"),
        "proxy_direction_model": {k: v for k, v in proxy.items() if k != "status"},
        "predictions": preds,
        "features_snapshot": snap,
    }
    append_ledger(record)


def evaluate_ledger() -> pd.DataFrame:
    if not config.LEDGER_PATH.exists():
        return pd.DataFrame()
    records = [json.loads(line) for line in open(config.LEDGER_PATH)]
    if not records:
        return pd.DataFrame()
    rows = []
    for rec in records:
        for pred in rec.get("predictions", []):
            due = pd.Timestamp(rec["run_date"]) + pd.Timedelta(days=pred["horizon_days"])
            rows.append({
                "run_date": rec["run_date"],
                "target": pred["target"],
                "p_model": pred["p_model"],
                "p_constant": pred["p_constant"],
                "outcome_due": str(due.date()),
            })
    ledger_df = pd.DataFrame(rows)

    market = storage.read_table("market_prices")
    if market is None or market.empty:
        return pd.DataFrame()
    closes = market_closes(market)
    idx = _ai_index(closes).dropna()

    outcomes = []
    for _, row in ledger_df.iterrows():
        base_dates = [d for d in idx.index if d <= pd.Timestamp(row["run_date"])]
        future_dates = [d for d in idx.index if d >= pd.Timestamp(row["outcome_due"])]
        if not base_dates or not future_dates:
            continue
        start_v, end_v = float(idx.loc[base_dates[-1]]), float(idx.loc[future_dates[0]])
        outcomes.append(1.0 if end_v / start_v - 1 > 0 else 0.0)
    ledger_df["outcome"] = pd.Series(outcomes)

    scored = ledger_df.dropna(subset=["outcome"])
    if scored.empty:
        return pd.DataFrame()
    summary = []
    for target, grp in scored.groupby("target"):
        for model_col in ["p_model", "p_constant"]:
            valid = grp.dropna(subset=[model_col])
            if valid.empty:
                continue
            summary.append({
                "target": target,
                "model": model_col,
                "n": len(valid),
                "brier": round(float(((valid[model_col] - valid["outcome"]) ** 2).mean()), 4),
                "accuracy": round(float(((valid[model_col] > 0.5).astype(float) == valid["outcome"]).mean()), 3),
            })
    return pd.DataFrame(summary)
