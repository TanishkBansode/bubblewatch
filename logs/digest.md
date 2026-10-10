# BubbleWatch Daily Digest — 2026-10-10 06:46 UTC

## Verdict
- **Bubble temperature:** **61/100** (hot) — gauge coverage 100%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **52%** (test Brier 0.2926 vs majority acc 0.563, asof 2026-10-09)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-09 |
| Bubble temperature (0-100) | 60.90 |
| Temperature change vs 1wk ago (pts) | -0.40 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | 0.05 |
| AI complex momentum 60d | 0.19 |
| Drawdown from 250d high | -0.01 |
| AI complex vs SPY 60d excess | 0.15 |
| AI complex vs equal-weight S&P 60d | 0.19 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.05 |
| Power/utilities theme momentum 60d | 0.04 |
| BTC momentum 30d (risk appetite) | 0.03 |
| US HY credit spread OAS (%) | 3.15 |
| HY spread change 5d (pts) | 0.05 |
| Credit spread data as-of | 2026-10-08 |
| VIX close | 14.84 |
| US 10Y yield proxy (%) | 5.24 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 102 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.52 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24721 | total=25858 new_days=1 src=yfinance |
| fred | ok | 24 | total=1443 latest={'hy_oas': '2026-10-08', 'vix_cls': '2026-10-08'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  50 |   0.293 |       0.34 |
| AI_complex_dir_5d | p_constant |  50 |   0.25  |       0.34 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*