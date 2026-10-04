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


def make_supervised(feats: pd.DataFrame, idx: pd.Series, x_cols: list[str] | None = None) -> pd.DataFrame:
    df = feats.copy()
    fwd = idx.reindex(df.index).shift(-HORIZON_DAYS) / idx.reindex(df.index) - 1.0
    # NaN-safe: (NaN > 0) is False, which used to label the most recent rows as "down".
    df["target_up"] = (fwd > 0).astype(float).where(fwd.notna())
    cols = x_cols if x_cols is not None else [c for c in MODEL_FEATURES if c in df.columns]
    df = df.dropna(subset=cols)
    df = df.dropna(subset=["target_up"])
    return df


def _skill_label(model_brier: float, const_brier: float, n: int) -> str:
    if n < 30:
        return "too_early"
    if model_brier < const_brier - 0.005:
        return "edge"
    if model_brier > const_brier + 0.005:
        return "worse"
    return "none"


def train_direction_model() -> dict:
    market = storage.read_table("market_prices")
    fred = storage.read_table("fred_daily")
    if market is None or market.empty:
        return {"status": "no_data"}
    closes = market_closes(market)
    idx = _ai_index(closes)
    feats = build_feature_frame(market, fred).dropna(how="all")
    feats = feats.dropna(subset=["ai_mom_60d"])
    if feats.empty:
        return {"status": "no_data"}

    # Only use features that exist on the latest row, so the forecast is about *today*.
    latest_row = feats.iloc[-1]
    x_cols = [c for c in MODEL_FEATURES if c in feats.columns and pd.notna(latest_row.get(c))]
    dropped = [c for c in MODEL_FEATURES if c not in x_cols]
    data = make_supervised(feats, idx, x_cols)
    if len(data) < 120 or not x_cols:
        return {"status": "insufficient_history", "rows": len(data)}

    split = int(len(data) * 0.8)
    X_train, y_train = data[x_cols].iloc[:split], data["target_up"].iloc[:split]
    X_test, y_test = data[x_cols].iloc[split:], data["target_up"].iloc[split:]

    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    model = make_pipeline(StandardScaler(), LogisticRegression(C=0.5, max_iter=1000))
    model.fit(X_train, y_train)

    result = {"status": "ok", "train_rows": int(split), "test_rows": int(len(y_test)),
              "features_used": x_cols, "features_dropped": dropped}
    if len(y_test) > 20:
        y = y_test.to_numpy()
        proba = model.predict_proba(X_test)[:, 1]
        brier = float(np.mean((proba - y) ** 2))
        const_brier = float(np.mean((0.5 - y) ** 2))
        acc = float(((proba > 0.5).astype(float) == y).mean())
        base = float(max(y.mean(), 1 - y.mean()))
        result.update({"brier": round(brier, 4),
                       "constant_brier": round(const_brier, 4),
                       "accuracy": round(acc, 3),
                       "majority_baseline_acc": round(base, 3),
                       "base_rate_up": round(float(y.mean()), 3),
                       "skill": _skill_label(brier, const_brier, len(y))})
    latest = feats[x_cols].iloc[[-1]]
    p_up = float(model.predict_proba(latest)[0, 1])
    result["p_ai_up_5d"] = round(p_up, 3)
    result["asof"] = str(feats.index[-1].date())
    result["trained_to"] = str(data.index[-1].date())
    return result


def direction_predictions(proxy: dict) -> list[dict]:
    ok = proxy.get("status") == "ok"
    p = proxy.get("p_ai_up_5d") if ok else None
    return [
        {
            "target": "AI_complex_dir_5d",
            "horizon_days": HORIZON_DAYS,
            "horizon_unit": "trading_days",
            "asof": proxy.get("asof") if ok else None,
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
    records = []
    for line in open(config.LEDGER_PATH):
        try:
            records.append(json.loads(line))
        except Exception:
            continue
    if not records:
        return pd.DataFrame()

    market = storage.read_table("market_prices")
    if market is None or market.empty:
        return pd.DataFrame()
    closes = market_closes(market)
    idx = _ai_index(closes).dropna()
    dates = list(idx.index)
    date_to_idx = {d: i for i, d in enumerate(dates)}

    rows = []
    for rec in records:
        run_d = pd.Timestamp(rec["run_date"])
        valid_dates = [d for d in dates if d <= run_d]
        if not valid_dates:
            continue
        base_d = valid_dates[-1]
        base_pos = date_to_idx[base_d]

        for pred in rec.get("predictions", []):
            h = int(pred.get("horizon_days", HORIZON_DAYS))
            unit = pred.get("horizon_unit", "calendar_days")
            outcome = None
            if "trading" in str(unit):
                target_pos = base_pos + h
                if target_pos < len(dates):
                    outcome = 1.0 if idx.iloc[target_pos] / idx.iloc[base_pos] - 1.0 > 0 else 0.0
            else:
                due = run_d + pd.Timedelta(days=h)
                future_dates = [d for d in dates if d >= due]
                if future_dates:
                    target_d = future_dates[0]
                    outcome = 1.0 if idx.loc[target_d] / idx.loc[base_d] - 1.0 > 0 else 0.0

            if outcome is not None:
                rows.append({
                    "run_date": rec["run_date"],
                    "target": pred.get("target", "AI_complex_dir_5d"),
                    "p_model": pred.get("p_model"),
                    "p_constant": pred.get("p_constant", 0.5),
                    "outcome": outcome,
                })

    if not rows:
        return pd.DataFrame()
    ledger_df = pd.DataFrame(rows)
    scored = ledger_df.dropna(subset=["outcome"])
    if scored.empty:
        return pd.DataFrame()

    summary = []
    for target, grp in scored.groupby("target"):
        for model_col, name in [("p_model", "p_model"), ("p_constant", "p_constant")]:
            valid = grp.dropna(subset=[model_col])
            if valid.empty:
                continue
            brier = float(((valid[model_col] - valid["outcome"]) ** 2).mean())
            acc = float(((valid[model_col] > 0.5).astype(float) == valid["outcome"]).mean())
            summary.append({
                "target": target,
                "model": name,
                "n": len(valid),
                "brier": round(brier, 4),
                "accuracy": round(acc, 3),
            })
    return pd.DataFrame(summary)

