from __future__ import annotations

import argparse
import traceback
from datetime import datetime, timezone

import pandas as pd

from . import config, features, lppls_model, models, regime as regime_module, report, storage
from .ingest import capex, equities, fred


def _recent_runs() -> list[dict]:
    path = config.LOGS_DIR / "runs.jsonl"
    if not path.exists():
        return []
    lines = path.read_text().strip().splitlines()
    today = datetime.now(timezone.utc).strftime(config.RUN_DATE_FMT)
    todays = [line for line in lines if f'"{today}' in line]
    keep, seen = [], set()
    for line in reversed(todays):
        import json

        d = json.loads(line)
        if d["source"] not in seen:
            seen.add(d["source"])
            keep.append(d)
    return list(reversed(keep))


def run(report_only: bool = False) -> None:
    if not report_only:
        for name, module in [
            ("equities", equities),
            ("fred", fred),
            ("capex", capex),
        ]:
            try:
                module.run()
            except Exception as exc:  # noqa: BLE001
                storage.log_run(name, "crashed", detail=f"{type(exc).__name__}: {exc}"[:200])
                traceback.print_exc()

    snap, alerts = features.current_snapshot()
    market = storage.read_table("market_prices")

    # Quantitative upgrades: HMM statistical regime detection & LPPLS bubble singularity
    if market is not None and not market.empty:
        closes = features.market_closes(market)
        rets = closes[[c for c in config.AI_COMPLEX if c in closes.columns]].mean(axis=1).pct_change().dropna()
        idx = features.basket_index(closes.pct_change(), config.AI_COMPLEX).dropna()

        # 1. HMM Statistical Regime Detection
        try:
            hmm_res = regime_module.detect_ai_regime(rets)
            if hmm_res.get("status") == "ok":
                snap["p_stress"] = hmm_res.get("p_stress")
                snap["p_expansion"] = hmm_res.get("p_expansion")
                snap["hmm_regime"] = hmm_res.get("regime_state")
                snap["hmm_persistence"] = hmm_res.get("persistence")
                if hmm_res.get("p_stress", 0) >= 0.80:
                    alerts.append(f"HMM statistical regime detects elevated volatility turbulence (P_stress = {hmm_res['p_stress']:.0%})")
        except Exception as exc:  # noqa: BLE001
            storage.log_run("hmm_regime", "error", detail=str(exc))

        # 2. LPPLS Crash Hazard Detection
        try:
            lppls_res = lppls_model.compute_lppls_hazard(idx)
            if lppls_res.get("status") == "ok":
                snap["lppls_confidence"] = lppls_res.get("confidence")
                snap["lppls_hazard_level"] = lppls_res.get("hazard_level")
                snap["lppls_median_tc_days"] = lppls_res.get("median_days_to_tc")
                if lppls_res.get("confidence", 0) >= 0.30:
                    tc_days = lppls_res.get("median_days_to_tc")
                    alerts.append(f"LPPLS bubble singularity detected ({lppls_res['confidence']:.0%} confidence; critical horizon ~{tc_days}d)")
        except Exception as exc:  # noqa: BLE001
            storage.log_run("lppls", "error", detail=str(exc))

    regime = features.classify_regime(snap)
    proxy = models.train_direction_model()
    preds = models.direction_predictions(proxy)

    try:
        features.build_and_store(snap)
    except Exception as exc:  # noqa: BLE001
        storage.log_run("features_store", "error", detail=str(exc))

    try:
        models.append_run_to_ledger(snap, regime, proxy, preds)
    except Exception as exc:  # noqa: BLE001
        storage.log_run("ledger", "error", detail=str(exc))

    leaderboard = None
    try:
        leaderboard = models.evaluate_ledger()
    except Exception as exc:  # noqa: BLE001
        storage.log_run("eval", "error", detail=str(exc))

    content = report.render(
        snap=snap,
        alerts=alerts,
        regime=regime,
        proxy=proxy,
        preds=preds,
        source_status=_recent_runs(),
        leaderboard=leaderboard,
    )
    out = report.write_digest(content)
    print(f"digest written: {out}")
    try:
        from . import webgen

        page = webgen.build(state={"proxy": proxy, "preds": preds})
        print(f"dashboard written: {page}")
    except Exception as exc:  # noqa: BLE001
        storage.log_run("webgen", "error", detail=f"{type(exc).__name__}: {exc}"[:200])
        traceback.print_exc()
    temp = snap.get("temperature")
    print(f"temperature={temp if temp is not None else '?'} band={snap.get('temperature_band', 'unknown')} regime={regime[0]}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="bubblewatch")
    parser.add_argument("command", choices=["run", "report", "eval"])
    args = parser.parse_args()
    if args.command == "run":
        run()
    elif args.command == "report":
        run(report_only=True)
    elif args.command == "eval":
        board = models.evaluate_ledger()
        print(board.to_string(index=False) if not board.empty else "no scored predictions yet")


if __name__ == "__main__":
    main()
