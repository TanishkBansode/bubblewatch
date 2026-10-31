from __future__ import annotations

import logging
from typing import Any
import numpy as np
import pandas as pd
from lppls.lppls import LPPLS

logger = logging.getLogger(__name__)


def compute_lppls_hazard(
    index_series: pd.Series,
    windows: list[int] | None = None,
    max_searches: int = 12,
) -> dict[str, Any]:
    """
    Fit Log-Periodic Power Law Singularity (LPPLS) model over rolling multiscale windows
    to estimate bubble acceleration and critical singularity time (t_c).

    Filtering criteria (Sornette & Filimonov standard):
      - 0.1 <= m <= 0.9 (super-exponential power law)
      - 4.0 <= omega <= 15.0 (log-periodic oscillation frequency)
      - B < 0 (upward acceleration)
      - t_c in (t2, t2 + 126] (projected singularity within 6 months)
      - O >= 2.0 (minimum log-periodic oscillations)

    Returns:
      confidence: fraction of windows with valid bubble singularity fits (0.0 to 1.0)
      hazard_level: 'none', 'low', 'elevated', 'critical'
      median_days_to_tc: estimated trading days until critical time (if confidence > 0)
      passing_fits: number of passing windows
      total_windows: total windows evaluated
    """
    clean_series = index_series.dropna()
    if len(clean_series) < 100:
        return {
            "status": "insufficient_history",
            "confidence": 0.0,
            "hazard_level": "none",
            "median_days_to_tc": None,
            "passing_fits": 0,
            "total_windows": 0,
        }

    if windows is None:
        # Default multiscale windows from ~4 months to ~1 year
        windows = [90, 120, 150, 180, 210, 240]

    usable_windows = [w for w in windows if w <= len(clean_series)]
    if not usable_windows:
        return {
            "status": "insufficient_history",
            "confidence": 0.0,
            "hazard_level": "none",
            "median_days_to_tc": None,
            "passing_fits": 0,
            "total_windows": 0,
        }

    log_prices = np.log(clean_series.to_numpy(dtype=float))
    total_len = len(log_prices)
    time_arr = np.arange(total_len, dtype=float)

    valid_fits = 0
    tc_offsets = []

    for w in usable_windows:
        w_time = time_arr[-w:]
        w_log_p = log_prices[-w:]

        # Shift time so t1=0 for numerical stability in optimizer
        t_start = float(w_time[0])
        shifted_time = w_time - t_start
        t2 = float(shifted_time[-1])

        obs = np.array([shifted_time, w_log_p])
        try:
            model = LPPLS(observations=obs)
            tc, m, omega, a, b, c, c1, c2, O, D = model.fit(max_searches=max_searches)

            is_super_exp = 0.1 <= float(m) <= 0.95
            is_valid_omega = 3.5 <= float(omega) <= 15.5
            is_accelerating = float(b) < 0
            is_forward_tc = t2 < float(tc) <= (t2 + 130)
            is_oscillating = float(O) >= 1.8

            if is_super_exp and is_valid_omega and is_accelerating and is_forward_tc and is_oscillating:
                valid_fits += 1
                tc_offsets.append(float(tc - t2))
        except Exception:
            continue

    total_w = len(usable_windows)
    confidence = float(valid_fits / total_w) if total_w > 0 else 0.0

    if confidence >= 0.50:
        hazard_level = "critical"
    elif confidence >= 0.30:
        hazard_level = "elevated"
    elif confidence >= 0.15:
        hazard_level = "low"
    else:
        hazard_level = "none"

    median_days = float(np.median(tc_offsets)) if tc_offsets else None

    return {
        "status": "ok",
        "confidence": round(confidence, 3),
        "hazard_level": hazard_level,
        "median_days_to_tc": round(median_days, 1) if median_days is not None else None,
        "passing_fits": valid_fits,
        "total_windows": total_w,
    }

