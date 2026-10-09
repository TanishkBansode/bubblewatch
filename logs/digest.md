# BubbleWatch Daily Digest — 2026-10-09 07:12 UTC

## Verdict
- **Bubble temperature:** **57/100** (warm) — gauge coverage 100%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **58%** (test Brier 0.2884 vs majority acc 0.563, asof 2026-10-08)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-08 |
| Bubble temperature (0-100) | 56.60 |
| Temperature change vs 1wk ago (pts) | -1.30 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | 0.06 |
| AI complex momentum 60d | 0.15 |
| Drawdown from 250d high | -0.02 |
| AI complex vs SPY 60d excess | 0.12 |
| AI complex vs equal-weight S&P 60d | 0.15 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.03 |
| Power/utilities theme momentum 60d | -0.04 |
| BTC momentum 30d (risk appetite) | 0.03 |
| US HY credit spread OAS (%) | 3.09 |
| HY spread change 5d (pts) | -0.15 |
| Credit spread data as-of | 2026-10-07 |
| VIX close | 15.41 |
| US 10Y yield proxy (%) | 5.23 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 101 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.58 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24721 | total=25825 new_days=1 src=yfinance |
| fred | ok | 24 | total=1441 latest={'hy_oas': '2026-10-07', 'vix_cls': '2026-10-07'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  45 |  0.2671 |      0.378 |
| AI_complex_dir_5d | p_constant |  45 |  0.25   |      0.378 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*