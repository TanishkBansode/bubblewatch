# BubbleWatch Daily Digest — 2026-10-27 06:03 UTC

## Verdict
- **Bubble temperature:** **36/100** (cool) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while still above deep-bear zone
- **Model** P(AI complex up next 5d): **55%** (test Brier 0.2928 vs majority acc 0.514, asof 2026-10-26)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-26 |
| Bubble temperature (0-100) | 35.80 |
| Temperature change vs 1wk ago (pts) | -7.10 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.06 |
| AI complex momentum 60d | 0.07 |
| Drawdown from 250d high | -0.10 |
| AI complex vs SPY 60d excess | 0.05 |
| AI complex vs equal-weight S&P 60d | 0.07 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.01 |
| Power/utilities theme momentum 60d | -0.02 |
| BTC momentum 30d (risk appetite) | 0.03 |
| US HY credit spread OAS (%) | 3.38 |
| HY spread change 5d (pts) | 0.09 |
| Credit spread data as-of | 2026-10-23 |
| VIX close | 18.39 |
| US 10Y yield proxy (%) | 4.99 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 119 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.55 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 23971 | total=26226 new_days=1 src=yfinance |
| fred | ok | 24 | total=1465 latest={'hy_oas': '2026-10-23', 'vix_cls': '2026-10-23'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  65 |  0.2882 |      0.308 |
| AI_complex_dir_5d | p_constant |  65 |  0.25   |      0.492 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*