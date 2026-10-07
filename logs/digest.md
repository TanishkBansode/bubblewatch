# BubbleWatch Daily Digest — 2026-10-07 06:57 UTC

## Verdict
- **Bubble temperature:** **63/100** (hot) — gauge coverage 100%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **43%** (test Brier 0.2809 vs majority acc 0.559, asof 2026-10-06)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-06 |
| Bubble temperature (0-100) | 63.10 |
| Temperature change vs 1wk ago (pts) | 2.20 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | 0.06 |
| AI complex momentum 60d | 0.18 |
| Drawdown from 250d high | 0.00 |
| AI complex vs SPY 60d excess | 0.13 |
| AI complex vs equal-weight S&P 60d | 0.18 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.05 |
| Power/utilities theme momentum 60d | 0.00 |
| BTC momentum 30d (risk appetite) | 0.08 |
| US HY credit spread OAS (%) | 3.12 |
| HY spread change 5d (pts) | 0.04 |
| Credit spread data as-of | 2026-10-05 |
| VIX close | 15.01 |
| US 10Y yield proxy (%) | 5.27 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 99 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.43 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24720 | total=25759 new_days=1 src=yfinance |
| fred | ok | 24 | total=1437 latest={'hy_oas': '2026-10-05', 'vix_cls': '2026-10-05'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  43 |  0.2678 |      0.372 |
| AI_complex_dir_5d | p_constant |  43 |  0.25   |      0.372 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*