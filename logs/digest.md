# BubbleWatch Daily Digest — 2026-10-14 05:54 UTC

## Verdict
- **Bubble temperature:** **60/100** (warm) — gauge coverage 100%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **53%** (test Brier 0.2918 vs majority acc 0.553, asof 2026-10-13)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-13 |
| Bubble temperature (0-100) | 59.90 |
| Temperature change vs 1wk ago (pts) | -5.90 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | 0.07 |
| AI complex momentum 60d | 0.18 |
| Drawdown from 250d high | -0.02 |
| AI complex vs SPY 60d excess | 0.13 |
| AI complex vs equal-weight S&P 60d | 0.17 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.04 |
| Power/utilities theme momentum 60d | 0.04 |
| BTC momentum 30d (risk appetite) | 0.06 |
| US HY credit spread OAS (%) | 3.11 |
| HY spread change 5d (pts) | 0.08 |
| Credit spread data as-of | 2026-10-12 |
| VIX close | 15.27 |
| US 10Y yield proxy (%) | 5.22 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 106 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.53 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24721 | total=25926 new_days=1 src=yfinance |
| fred | ok | 25 | total=1447 latest={'hy_oas': '2026-10-12', 'vix_cls': '2026-10-12'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  52 |  0.2857 |      0.365 |
| AI_complex_dir_5d | p_constant |  52 |  0.25   |      0.365 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*