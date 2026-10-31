from __future__ import annotations

import json
from typing import Any
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from . import config, storage
from .features import MODEL_FEATURES, basket_index, build_feature_frame, market_closes

HORIZON_DAYS = 5


def _ai_index(closes: pd.DataFrame) -> pd.Series:
    rets = closes.pct_change()
    return basket_index(rets, config.AI_COMPLEX)


def brier_decomposition(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 5) -> dict[str, float]:
    """
    Murphy (1973) Brier score calibration decomposition on binned probabilistic forecasts:
      Brier = Reliability - Resolution + Uncertainty
    where:
      Uncertainty = y_bar * (1 - y_bar) (intrinsic unpredictability of the event)
      Reliability = sum(n_k * (p_k - y_k)^2) / N (calibration error; 0 is perfect)
      Resolution  = sum(n_k * (y_k - y_bar)^2) / N (ability to discriminate outcomes; higher is better)
    """
    y = np.asarray(y_true, dtype=float)
    p = np.clip(np.asarray(y_prob, dtype=float), 1e-6, 1.0 - 1e-6)
    n = len(y)
    if n == 0:
        return {"brier": 0.0, "uncertainty": 0.0, "reliability": 0.0, "resolution": 0.0}

    y_bar = float(y.mean())
    unc = y_bar * (1.0 - y_bar)

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    bin_idx = np.digitize(p, bin_edges) - 1
    bin_idx = np.clip(bin_idx, 0, n_bins - 1)

    rel = 0.0
    res = 0.0
    for k in range(n_bins):
        mask = (bin_idx == k)
        nk = np.sum(mask)
        if nk > 0:
            pk = float(p[mask].mean())
            yk = float(y[mask].mean())
            rel += nk * ((pk - yk) ** 2)
            res += nk * ((yk - y_bar) ** 2)
    rel /= n
    res /= n
    brier = float(np.mean((p - y) ** 2))

    return {
        "brier": round(brier, 4),
        "uncertainty": round(unc, 4),
        "reliability": round(rel, 4),
        "resolution": round(res, 4),
    }


def make_supervised(
    feats: pd.DataFrame,
    idx: pd.Series,
    horizon_days: int = HORIZON_DAYS,
    x_cols: list[str] | None = None,
    is_tail_risk: bool = False,
    tail_threshold: float = -0.05,
) -> pd.DataFrame:
    """Build supervised training frame with clean forward targets."""
    df = feats.copy()
    fwd = idx.reindex(df.index).shift(-horizon_days) / idx.reindex(df.index) - 1.0

    if is_tail_risk:
        # 1 if drawdown meets or breaches threshold, 0 otherwise
        df["target"] = (fwd <= tail_threshold).astype(float).where(fwd.notna())
    else:
        # 1 if positive return, 0 otherwise
        df["target"] = (fwd > 0.0).astype(float).where(fwd.notna())

    cols = x_cols if x_cols is not None else [c for c in MODEL_FEATURES if c in df.columns]
    # Forward-fill any minor missing indicator up to 5 days, then median-impute to stabilize feature matrix
    for col in cols:
        if col in df.columns:
            df[col] = df[col].ffill(limit=5)
            med = df[col].median()
            df[col] = df[col].fillna(med if pd.notna(med) else 0.0)

    df = df.dropna(subset=cols)
    df = df.dropna(subset=["target"])
    return df


def _skill_label(model_brier: float, benchmark_brier: float, n: int) -> str:
    if n < 30:
        return "too_early"
    if model_brier < benchmark_brier - 0.005:
        return "edge"
    if model_brier > benchmark_brier + 0.005:
        return "worse"
    return "neutral"


def train_direction_model() -> dict[str, Any]:
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

    # Use available features with stable fallback
    x_cols = [c for c in MODEL_FEATURES if c in feats.columns]
    data = make_supervised(feats, idx, horizon_days=HORIZON_DAYS, x_cols=x_cols)
    if len(data) < 120 or not x_cols:
        return {"status": "insufficient_history", "rows": len(data)}

    # Purged Chronological Train/Test Split
    split = int(len(data) * 0.80)
    purge_gap = HORIZON_DAYS  # Purge training rows whose forward target spans into test window
    train_end = max(10, split - purge_gap)

    X_train = data[x_cols].iloc[:train_end]
    y_train = data["target"].iloc[:train_end]

    X_test = data[x_cols].iloc[split:]
    y_test = data["target"].iloc[split:]

    # Regularized L2 pipeline with feature standard scaling
    model = make_pipeline(StandardScaler(), LogisticRegression(C=0.15, max_iter=1000))
    model.fit(X_train, y_train)

    train_base_rate = float(y_train.mean())
    result: dict[str, Any] = {
        "status": "ok",
        "train_rows": int(len(X_train)),
        "test_rows": int(len(y_test)),
        "purged_rows": int(purge_gap),
        "features_used": x_cols,
        "features_dropped": [c for c in MODEL_FEATURES if c not in x_cols],
        "train_base_rate": round(train_base_rate, 3),
    }

    if len(y_test) > 20:
        y = y_test.to_numpy()
        proba = model.predict_proba(X_test)[:, 1]
        brier = float(np.mean((proba - y) ** 2))
        base_rate_brier = float(np.mean((train_base_rate - y) ** 2))
        coinflip_brier = float(np.mean((0.5 - y) ** 2))
        acc = float(((proba > 0.5).astype(float) == y).mean())
        majority_acc = float(max(y.mean(), 1.0 - y.mean()))

        decomp = brier_decomposition(y, proba)

        result.update(
            {
                "brier": round(brier, 4),
                "base_rate_brier": round(base_rate_brier, 4),
                "constant_brier": round(coinflip_brier, 4),
                "brier_uncertainty": decomp["uncertainty"],
                "brier_reliability": decomp["reliability"],
                "brier_resolution": decomp["resolution"],
                "accuracy": round(acc, 3),
                "majority_baseline_acc": round(majority_acc, 3),
                "test_base_rate_up": round(float(y.mean()), 3),
                "skill": _skill_label(brier, base_rate_brier, len(y)),
                "skill_vs_coinflip": _skill_label(brier, coinflip_brier, len(y)),
            }
        )

    # Refit full historical sample for current live prediction
    full_model = make_pipeline(StandardScaler(), LogisticRegression(C=0.15, max_iter=1000))
    full_model.fit(data[x_cols], data["target"])

    latest = feats[x_cols].iloc[[-1]].copy()
    for col in x_cols:
        if latest[col].isna().any():
            latest[col] = latest[col].fillna(data[col].median())

    p_up_5d = float(full_model.predict_proba(latest)[0, 1])
    result["p_ai_up_5d"] = round(p_up_5d, 3)

    # Train 21-day directional model
    data_21d = make_supervised(feats, idx, horizon_days=21, x_cols=x_cols)
    if len(data_21d) >= 120:
        m21 = make_pipeline(StandardScaler(), LogisticRegression(C=0.15, max_iter=1000))
        m21.fit(data_21d[x_cols], data_21d["target"])
        result["p_ai_up_21d"] = round(float(m21.predict_proba(latest)[0, 1]), 3)

    # Train 21-day tail risk model (drawdown <= -5%)
    data_tail21 = make_supervised(feats, idx, horizon_days=21, x_cols=x_cols, is_tail_risk=True, tail_threshold=-0.05)
    if len(data_tail21) >= 120:
        mtail21 = make_pipeline(StandardScaler(), LogisticRegression(C=0.15, max_iter=1000))
        mtail21.fit(data_tail21[x_cols], data_tail21["target"])
        result["p_tail_down_5pct_21d"] = round(float(mtail21.predict_proba(latest)[0, 1]), 3)

    result["asof"] = str(feats.index[-1].date())
    result["trained_to"] = str(data.index[-1].date())
    return result


def direction_predictions(proxy: dict[str, Any]) -> list[dict[str, Any]]:
    ok = proxy.get("status") == "ok"
    p5 = proxy.get("p_ai_up_5d") if ok else None
    p21 = proxy.get("p_ai_up_21d") if ok else None
    ptail21 = proxy.get("p_tail_down_5pct_21d") if ok else None
    base5 = proxy.get("train_base_rate", 0.59)

    preds: list[dict[str, Any]] = [
        {
            "target": "AI_complex_dir_5d",
            "horizon_days": 5,
            "horizon_unit": "trading_days",
            "asof": proxy.get("asof") if ok else None,
            "p_model": p5,
            "p_constant": 0.5,
            "p_base_rate": base5,
            "note": "regularized logistic on equity+credit+breadth; purged train/test",
        }
    ]

    if p21 is not None:
        preds.append(
            {
                "target": "AI_complex_dir_21d",
                "horizon_days": 21,
                "horizon_unit": "trading_days",
                "asof": proxy.get("asof") if ok else None,
                "p_model": p21,
                "p_constant": 0.5,
                "note": "21-trading-day direction forecast (~1 month)",
            }
        )

    if ptail21 is not None:
        preds.append(
            {
                "target": "AI_complex_tail_21d",
                "horizon_days": 21,
                "horizon_unit": "trading_days",
                "asof": proxy.get("asof") if ok else None,
                "p_model": ptail21,
                "p_constant": 0.15,
                "note": "21-trading-day tail risk hazard: P(return <= -5%)",
            }
        )

    return preds


def append_run_to_ledger(
    snap: dict[str, Any],
    regime: tuple[str, str],
    proxy: dict[str, Any],
    preds: list[dict[str, Any]],
) -> None:
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
            target = pred.get("target", "AI_complex_dir_5d")
            outcome = None

            if "trading" in str(unit):
                target_pos = base_pos + h
                if target_pos < len(dates):
                    ret = idx.iloc[target_pos] / idx.iloc[base_pos] - 1.0
                    if "tail" in target:
                        outcome = 1.0 if ret <= -0.05 else 0.0
                    else:
                        outcome = 1.0 if ret > 0.0 else 0.0
            else:
                due = run_d + pd.Timedelta(days=h)
                future_dates = [d for d in dates if d >= due]
                if future_dates:
                    target_d = future_dates[0]
                    ret = idx.loc[target_d] / idx.loc[base_d] - 1.0
                    if "tail" in target:
                        outcome = 1.0 if ret <= -0.05 else 0.0
                    else:
                        outcome = 1.0 if ret > 0.0 else 0.0

            if outcome is not None:
                rows.append({
                    "run_date": rec["run_date"],
                    "target": target,
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
