from __future__ import annotations

import numpy as np
import pandas as pd

from . import config, storage

MODEL_FEATURES = [
    "ai_mom_20d", "ai_mom_60d", "ai_drawdown_250d",
    "rs_ai_spx_60d", "rs_ai_rsp_60d", "rs_spy_rsp_60d",
    "power_mom_60d", "btc_mom_30d", "hy_oas_chg_5d", "vix_chg_5d",
]


def market_closes(market: pd.DataFrame) -> pd.DataFrame:
    closes = market.pivot_table(index="date", columns="symbol", values="close", aggfunc="last")
    closes.index = pd.to_datetime(closes.index)
    return closes.sort_index().ffill()


def basket_index(rets: pd.DataFrame, members: list[str]) -> pd.Series:
    cols = [t for t in members if t in rets.columns]
    mean_ret = rets[cols].mean(axis=1)
    idx = (1.0 + mean_ret.fillna(0.0)).cumprod()
    start = mean_ret.first_valid_index()
    if start is not None:
        idx.loc[idx.index < start] = np.nan
    return idx


def build_feature_frame(market: pd.DataFrame, fred: pd.DataFrame | None) -> pd.DataFrame:
    closes = market_closes(market)
    rets = closes.pct_change()

    ai_idx = basket_index(rets, config.AI_COMPLEX)
    ai_cols = [c for c in config.AI_COMPLEX if c in rets.columns]
    ai_ret_mean = rets[ai_cols].mean(axis=1)

    def _sum60(sym: str) -> pd.Series:
        return rets[sym].rolling(60, min_periods=40).sum()

    feats = pd.DataFrame(index=closes.index)
    feats["ai_mom_20d"] = ai_idx.pct_change(20)
    feats["ai_mom_60d"] = ai_idx.pct_change(60)
    roll_max = ai_idx.rolling(250, min_periods=60).max()
    feats["ai_drawdown_250d"] = ai_idx / roll_max - 1.0

    if "SPY" in rets.columns:
        feats["rs_ai_spx_60d"] = ai_ret_mean.rolling(60, min_periods=40).sum() - _sum60("SPY")
    if "RSP" in rets.columns:
        feats["rs_ai_rsp_60d"] = ai_ret_mean.rolling(60, min_periods=40).sum() - _sum60("RSP")
        if "SPY" in rets.columns:
            feats["rs_spy_rsp_60d"] = _sum60("SPY") - _sum60("RSP")
    power = basket_index(rets, config.POWER_THEME)
    feats["power_mom_60d"] = power.pct_change(60)

    if "BTC-USD" in closes.columns:
        feats["btc_mom_30d"] = closes["BTC-USD"].pct_change(30)

    if fred is not None and not fred.empty:
        wide = fred.pivot_table(index="date", columns="series", values="value", aggfunc="last")
        wide.index = pd.to_datetime(wide.index)
        wide = wide.sort_index()
        if "hy_oas" in wide.columns:
            feats["hy_oas"] = wide["hy_oas"].reindex(feats.index).ffill(limit=5)
            feats["hy_oas_chg_5d"] = feats["hy_oas"].diff(5)
        if "vix_cls" in wide.columns:
            feats["vix_cls"] = wide["vix_cls"].reindex(feats.index).ffill(limit=5)
            feats["vix_chg_5d"] = feats["vix_cls"].diff(5)
    if "^TNX" in closes.columns and "vix_cls" not in feats.columns:
        raw = closes["^TNX"].dropna()
        scale = 10.0 if float(raw.median()) > 20 else 1.0
        feats["rate_10y_proxy"] = closes["^TNX"] / scale

    return add_temperature(feats)


def _zscores(frame: pd.DataFrame) -> pd.DataFrame:
    z = pd.DataFrame(index=frame.index)

    def _roll_z(col: str) -> pd.Series:
        if col not in frame.columns or frame[col].notna().sum() < 30:
            return pd.Series(np.nan, index=frame.index)
        return frame[col].rolling(250, min_periods=100).apply(
            lambda w: (w.iloc[-1] - w.mean()) / (w.std() or np.nan), raw=False
        )

    z["z_mom_stretch"] = _roll_z("ai_mom_60d")
    z["z_rs_eqw"] = _roll_z("rs_ai_rsp_60d")
    z["z_concentration"] = _roll_z("rs_spy_rsp_60d")
    z["z_credit_tightness"] = -_roll_z("hy_oas")
    z["z_dd_proximity"] = -_roll_z("ai_drawdown_250d")
    z["z_btc_risk"] = _roll_z("btc_mom_30d")
    return z


def add_temperature(feats: pd.DataFrame) -> pd.DataFrame:
    z = _zscores(feats)
    out = feats.copy()
    for col in z.columns:
        out[col] = z[col].clip(-2.0, 2.0)
    weights = config.TEMP_WEIGHTS
    total_w_present = pd.Series(0.0, index=out.index)
    weighted = pd.Series(0.0, index=out.index)
    for col, w in weights.items():
        present = out[col].notna()
        weighted.loc[present] += w * out.loc[present, col]
        total_w_present.loc[present] += w
    mean_wz = weighted / total_w_present.where(total_w_present > 0)
    conf = (total_w_present / sum(weights.values())).clip(0, 1)
    out["temperature"] = (50.0 + 25.0 * mean_wz).clip(0, 100)
    out["temp_confidence"] = conf
    return out


def temperature_band(temp: float | None) -> str:
    if temp is None or np.isnan(temp):
        return "unknown"
    if temp < 25:
        return "frost"
    if temp < 45:
        return "cool"
    if temp < 60:
        return "warm"
    if temp < 75:
        return "hot"
    return "euphoric"


def classify_regime(snap: dict) -> tuple[str, str]:
    dd = snap.get("ai_drawdown_250d")
    m20 = snap.get("ai_mom_20d")
    m60 = snap.get("ai_mom_60d")
    temp = snap.get("temperature")
    if dd is None or m20 is None or m60 is None:
        return "unknown", "insufficient market history"
    if dd <= -0.30 and m20 > 0:
        return "capitulation_recovery", f"drawdown {dd:.0%} with 20d momentum turning up"
    if dd <= -0.25:
        return "contraction", f"AI complex in deep drawdown ({dd:.0%})"
    if m20 < 0 and dd > -0.25:
        return "distribution", "short-term momentum rolled over while still above deep-bear zone"
    if temp is not None and temp >= 70 and m60 > 0:
        return "euphoria", f"temperature {temp:.0f} with intact 60d trend"
    if m60 > 0:
        return "expansion", "uptrend intact without froth extremes"
    return "neutral", f"mixed tape: 60d momentum {m60:+.1%}, drawdown {dd:.0%}"


def capex_features(capex: pd.DataFrame | None) -> dict:
    out = {"capex_usd_b": None, "capex_yoy_pct": None, "nvda_rev_yoy_pct": None,
           "nvda_decel_pts": None, "capex_age_days": None}
    if capex is None or capex.empty:
        return out
    df = capex.sort_values("period").reset_index(drop=True)
    latest = df.iloc[-1]
    out["capex_usd_b"] = None if pd.isna(latest.get("hyperscaler_capex_usd_b")) else round(float(latest["hyperscaler_capex_usd_b"]), 1)
    out["nvda_rev_yoy_pct"] = None if pd.isna(latest.get("nvda_rev_yoy_pct")) else round(float(latest["nvda_rev_yoy_pct"]), 1)
    if len(df) >= 5 and pd.notna(latest["hyperscaler_capex_usd_b"]) and pd.notna(df.iloc[-5]["hyperscaler_capex_usd_b"]):
        prev = float(df.iloc[-5]["hyperscaler_capex_usd_b"])
        if prev > 0:
            out["capex_yoy_pct"] = round((float(latest["hyperscaler_capex_usd_b"]) / prev - 1) * 100, 1)
    if len(df) >= 2 and out["nvda_rev_yoy_pct"] is not None and pd.notna(df.iloc[-2]["nvda_rev_yoy_pct"]):
        out["nvda_decel_pts"] = round(out["nvda_rev_yoy_pct"] - float(df.iloc[-2]["nvda_rev_yoy_pct"]), 1)
    try:
        year, quarter = latest["period"].split("Q")
        quarter_end_month = int(quarter) * 3
        end = pd.Timestamp(int(year), quarter_end_month, 1) + pd.offsets.QuarterEnd(0)
        out["capex_age_days"] = int((pd.Timestamp.utcnow().normalize() - end.normalize()).days)
    except Exception:
        pass
    return out


def current_snapshot() -> tuple[dict, list[str]]:
    market = storage.read_table("market_prices")
    fred = storage.read_table("fred_daily")
    capex = storage.read_table("capex_quarterly")

    snap: dict = {}
    alerts: list[str] = []

    frame = pd.DataFrame()
    if market is not None and not market.empty:
        frame = build_feature_frame(market, fred)
        valid = frame.dropna(subset=["ai_mom_60d"], how="any")
        if not valid.empty:
            last = valid.iloc[-1]
            for col in ["ai_mom_20d", "ai_mom_60d", "ai_drawdown_250d", "rs_ai_spx_60d",
                        "rs_ai_rsp_60d", "rs_spy_rsp_60d", "power_mom_60d", "btc_mom_30d",
                        "hy_oas", "hy_oas_chg_5d", "vix_cls", "vix_chg_5d",
                        "temperature", "temp_confidence"]:
                if col in last.index and pd.notna(last[col]):
                    snap[col] = round(float(last[col]), 4)
            snap["temperature"] = round(float(last["temperature"]), 1)
            for gcol in ["z_mom_stretch", "z_rs_eqw", "z_concentration",
                         "z_credit_tightness", "z_dd_proximity", "z_btc_risk"]:
                if pd.notna(last[gcol]):
                    snap[gcol] = round(float(last[gcol]), 3)

    snap.update({k: v for k, v in capex_features(capex).items()})

    temp = snap.get("temperature")
    if temp is not None:
        band = temperature_band(temp)
        snap["temperature_band"] = band
        if temp >= 70:
            alerts.append(f"Bubble temperature in froth zone ({temp:.0f}/100)")
        elif temp <= 25:
            alerts.append(f"Ice zone ({temp:.0f}/100): extreme pessimism often marks late-stage selloffs")
    oas_chg = snap.get("hy_oas_chg_5d")
    if oas_chg is not None and oas_chg >= 0.4:
        alerts.append(f"HY spreads jumped +{oas_chg * 100:.0f}bp in 5 days — credit stress")
    dd = snap.get("ai_drawdown_250d")
    if dd is not None and dd <= -0.25:
        alerts.append(f"AI complex drawdown {dd:.0%} from highs")
    decel = snap.get("nvda_decel_pts")
    if decel is not None and decel <= -15:
        alerts.append(f"NVDA revenue growth decelerated {decel:+.0f}pts QoQ")
    age = snap.get("capex_age_days")
    if age is not None and age > 200:
        alerts.append(f"Fundamentals anchor stale ({age}d old) — append new quarter to data/manual/hyperscaler_capex.csv")
    return snap, alerts


def build_and_store(snap: dict) -> None:
    df = pd.DataFrame([{"date": pd.Timestamp.utcnow().strftime(config.RUN_DATE_FMT),
                        **{k: v for k, v in sorted(snap.items())}}])
    storage.write_table(df, "features_daily", ["date"])
