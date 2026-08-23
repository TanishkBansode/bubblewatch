from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import config

FEATURE_LABELS = [
    ("temperature", "Bubble temperature (0-100)"),
    ("temp_confidence", "Gauge coverage"),
    ("ai_mom_20d", "AI complex momentum 20d"),
    ("ai_mom_60d", "AI complex momentum 60d"),
    ("ai_drawdown_250d", "Drawdown from 250d high"),
    ("rs_ai_spx_60d", "AI complex vs SPY 60d excess"),
    ("rs_ai_rsp_60d", "AI complex vs equal-weight S&P 60d"),
    ("rs_spy_rsp_60d", "Cap-vs-equal-weight spread 60d (concentration)"),
    ("power_mom_60d", "Power/utilities theme momentum 60d"),
    ("btc_mom_30d", "BTC momentum 30d (risk appetite)"),
    ("hy_oas", "US HY credit spread OAS (%)"),
    ("hy_oas_chg_5d", "HY spread change 5d (pts)"),
    ("vix_cls", "VIX close"),
    ("rate_10y_proxy", "US 10Y yield proxy (%)"),
    ("capex_usd_b", "Hyperscaler capex, latest qtr ($B)"),
    ("capex_yoy_pct", "Hyperscaler capex YoY (%)"),
    ("nvda_rev_yoy_pct", "NVDA revenue YoY (%)"),
    ("nvda_decel_pts", "NVDA YoY deceleration QoQ (pts)"),
    ("capex_age_days", "Days since fundamentals anchor quarter-end"),
]


def _fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:,.2f}"
    return str(v)


def render(snap: dict, alerts: list[str], regime: tuple[str, str],
           proxy: dict, preds: list[dict], source_status: list[dict],
           leaderboard: pd.DataFrame | None) -> str:
    lines = []
    temp = snap.get("temperature")
    band = snap.get("temperature_band", "unknown")
    lines.append(f"# BubbleWatch Daily Digest — {pd.Timestamp.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    lines.append("## Verdict")
    if temp is not None:
        lines.append(f"- **Bubble temperature:** **{temp:.0f}/100** ({band}) — gauge coverage {snap.get('temp_confidence', 0):.0%}")
    else:
        lines.append("- **Bubble temperature:** warming up (insufficient history for z-scores)")
    lines.append(f"- **Regime:** `{regime[0]}` — {regime[1]}")
    if proxy.get("status") == "ok":
        lines.append(
            f"- **Model** P(AI complex up next 5d): **{proxy['p_ai_up_5d']:.0%}** "
            f"(test Brier {proxy.get('brier', '-')} vs majority acc {proxy.get('majority_baseline_acc', '-')}, asof {proxy.get('asof', '?')})"
        )
    else:
        lines.append(f"- **Direction model:** unavailable ({proxy.get('status')})")
    lines.append("")

    lines.append("## Key indicators")
    lines.append("| Indicator | Value |")
    lines.append("|---|---|")
    for key, label in FEATURE_LABELS:
        if key in snap:
            lines.append(f"| {label} | {_fmt(snap[key])} |")
    lines.append("")

    if preds:
        lines.append("## Today's predictions (logged to ledger)")
        lines.append("| Target | Horizon | Model P(up) | Constant baseline | Note |")
        lines.append("|---|---|---|---|---|")
        for p in preds:
            pm = f"{p['p_model']:.2f}" if p["p_model"] is not None else "-"
            lines.append(f"| {p['target']} | {p['horizon_days']}d | {pm} | {p['p_constant']:.2f} | {p['note']} |")
        lines.append("")

    if alerts:
        lines.append("## Alerts")
        for a in alerts:
            lines.append(f"- ⚠️ {a}")
        lines.append("")

    lines.append("## Source status (this run)")
    lines.append("| Source | Status | Rows | Detail |")
    lines.append("|---|---|---|---|")
    for s in source_status:
        lines.append(f"| {s['source']} | {s['status']} | {s['rows']} | {s['detail'][:80]} |")
    lines.append("")

    if leaderboard is not None and not leaderboard.empty:
        lines.append("## Prediction scoreboard (vs baselines)")
        lines.append(leaderboard.to_markdown(index=False))
        lines.append("")

    lines.append("---")
    lines.append("*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*")
    return "\n".join(lines)


def write_digest(content: str) -> Path:
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    out = config.LOGS_DIR / "digest.md"
    out.write_text(content)
    return out
