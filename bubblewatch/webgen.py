from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

from . import config, features, models, storage
from .features import basket_index, market_closes

_WEB_DIR = config.BASE_DIR / "web"
_TEMPLATE = Path(__file__).parent / "templates" / "dashboard.html"
_PLACEHOLDER = "__BUBBLEWATCH_PAYLOAD__"
_STATIC_PAGES = ["about.html", "guide.html", "method.html"]


def _rebased(closes: pd.DataFrame, series: dict[str, pd.Series]) -> dict:
    if not series:
        return {}
    starts = []
    for s in series.values():
        valid = s.dropna()
        if not valid.empty:
            starts.append(valid.index[0])
    if not starts:
        return {}
    common_start = min(starts)
    full = closes.index[closes.index >= common_start]
    out = {"dates": [d.strftime("%Y-%m-%d") for d in full]}
    for name, s in series.items():
        s2 = s.reindex(full).ffill()
        first_valid = s2.first_valid_index()
        if first_valid is None:
            out[name] = [None] * len(full)
            continue
        base = float(s2.loc[first_valid])
        out[name] = [
            round(float(v) / base * 100.0, 2) if pd.notna(v) else None
            for v in s2
        ]
    return out


def _chart_frames(market: pd.DataFrame) -> dict:
    closes = market_closes(market)
    rets = closes.pct_change()
    ai_idx = basket_index(rets, config.AI_COMPLEX).dropna()

    trio_series = {"ai": ai_idx}
    if "SPY" in closes.columns:
        trio_series["spx"] = closes["SPY"]
    if "RSP" in closes.columns:
        trio_series["eqw"] = closes["RSP"]
    rebase = _rebased(closes, trio_series)

    duo = {"ai": ai_idx}
    power = basket_index(rets, config.POWER_THEME)
    if not power.dropna().empty:
        duo["power"] = power
    theme = _rebased(closes, duo)

    fred = storage.read_table("fred_daily")
    oas = {"dates": [], "values": []}
    temp = {"dates": [], "values": []}
    frame = features.build_feature_frame(market, fred)
    valid = frame.dropna(subset=["temperature"])
    if not valid.empty:
        temp = {
            "dates": valid.index.strftime("%Y-%m-%d").tolist(),
            "values": [round(float(v), 1) for v in valid["temperature"]],
        }
    if fred is not None and not fred.empty and "hy_oas" in frame.columns:
        oas_valid = frame.dropna(subset=["hy_oas"])
        if not oas_valid.empty:
            oas = {
                "dates": oas_valid.index.strftime("%Y-%m-%d").tolist(),
                "values": [round(float(v), 3) for v in oas_valid["hy_oas"]],
            }
    return {"rebase": rebase, "theme": theme, "temp": temp, "oas": oas}


def _indicator_rows(snap: dict) -> list[dict]:
    from .report import FEATURE_LABELS

    rows = []
    for key, label in FEATURE_LABELS:
        if key not in snap:
            continue
        v = snap[key]
        if isinstance(v, float):
            val = round(v * 100, 2) if key.endswith(("_20d", "_60d", "_30d", "_250d")) and key != "rs_spy_rsp_60d" and abs(v) <= 5 else round(v, 2)
        else:
            val = v
        rows.append({"label": label, "value": val})
    return rows


def _fundamentals(capex: pd.DataFrame | None) -> dict:
    if capex is None or capex.empty:
        return {}
    df = capex.sort_values("period")
    return {
        "periods": df["period"].tolist(),
        "capex": [None if pd.isna(v) else round(float(v), 1) for v in df["hyperscaler_capex_usd_b"]],
        "nvda_yoy": [None if pd.isna(v) else round(float(v), 1) for v in df["nvda_rev_yoy_pct"]],
    }


def _ledger_rows(limit: int = 30) -> list[dict]:
    if not config.LEDGER_PATH.exists():
        return []
    rows = []
    for line in open(config.LEDGER_PATH):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        for pred in rec.get("predictions", []):
            rows.append({
                "date": rec.get("run_date"),
                "target": pred.get("target"),
                "p_model": pred.get("p_model"),
                "p_const": pred.get("p_constant"),
                "regime": rec.get("regime"),
                "temperature": rec.get("temperature"),
            })
    return rows[-limit:]


def build(state: dict | None = None) -> Path:
    market = storage.read_table("market_prices")
    capex = storage.read_table("capex_quarterly")

    snap, alerts = features.current_snapshot()
    regime = features.classify_regime(snap)
    proxy = (state or {}).get("proxy") or models.train_direction_model()
    preds = (state or {}).get("preds") or models.direction_predictions(proxy)

    charts = _chart_frames(market) if market is not None and not market.empty else {}

    scoreboard: list[dict] = []
    try:
        board = models.evaluate_ledger()
        if not board.empty:
            scoreboard = board.to_dict(orient="records")
    except Exception:
        pass

    payload = {
        "generated": pd.Timestamp.utcnow().isoformat(timespec="seconds"),
        "modelVersion": config.MODEL_VERSION,
        "snap": snap,
        "alerts": alerts,
        "regime": {"label": regime[0], "reason": regime[1]},
        "proxy": proxy,
        "preds": preds,
        "charts": charts,
        "indicators": _indicator_rows(snap),
        "fundamentals": _fundamentals(capex),
        "ledger": _ledger_rows(),
        "scoreboard": scoreboard,
    }

    html = _TEMPLATE.read_text().replace(_PLACEHOLDER, json.dumps(payload, default=str).replace("</", "<\\/"))
    _WEB_DIR.mkdir(parents=True, exist_ok=True)
    for page in _STATIC_PAGES:
        shutil.copyfile(_TEMPLATE.parent / page, _WEB_DIR / page)
    out = _WEB_DIR / "index.html"
    out.write_text(html)
    return out
