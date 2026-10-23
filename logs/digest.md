# BubbleWatch Daily Digest — 2026-10-23 05:49 UTC

## Verdict
- **Bubble temperature:** **42/100** (cool) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while still above deep-bear zone
- **Model** P(AI complex up next 5d): **65%** (test Brier 0.2926 vs majority acc 0.533, asof 2026-10-22)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-22 |
| Bubble temperature (0-100) | 42.30 |
| Temperature change vs 1wk ago (pts) | -1.80 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.08 |
| AI complex momentum 60d | 0.14 |
| Drawdown from 250d high | -0.11 |
| AI complex vs SPY 60d excess | 0.09 |
| AI complex vs equal-weight S&P 60d | 0.13 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.04 |
| Power/utilities theme momentum 60d | -0.00 |
| BTC momentum 30d (risk appetite) | 0.08 |
| US HY credit spread OAS (%) | 3.27 |
| HY spread change 5d (pts) | 0.04 |
| Credit spread data as-of | 2026-10-21 |
| VIX close | 19.03 |
| US 10Y yield proxy (%) | 4.95 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 115 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.65 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24721 | total=26159 new_days=1 src=yfinance |
| fred | ok | 24 | total=1461 latest={'hy_oas': '2026-10-21', 'vix_cls': '2026-10-21'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  61 |  0.2842 |      0.328 |
| AI_complex_dir_5d | p_constant |  61 |  0.25   |      0.459 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*