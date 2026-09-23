# BubbleWatch Daily Digest — 2026-09-23 05:38 UTC

## Verdict
- **Bubble temperature:** **61/100** (hot) — gauge coverage 80%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **46%** (test Brier 0.2987 vs majority acc 0.662, asof 2026-08-25)

## Key indicators
| Indicator | Value |
|---|---|
| Bubble temperature (0-100) | 61.40 |
| Gauge coverage | 0.80 |
| AI complex momentum 20d | 0.05 |
| AI complex momentum 60d | 0.18 |
| Drawdown from 250d high | 0.00 |
| AI complex vs SPY 60d excess | 0.12 |
| AI complex vs equal-weight S&P 60d | 0.17 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.05 |
| Power/utilities theme momentum 60d | -0.11 |
| BTC momentum 30d (risk appetite) | 0.10 |
| Hyperscaler capex, latest qtr ($B) | 88.00 |
| Hyperscaler capex YoY (%) | 65.40 |
| NVDA revenue YoY (%) | 56.00 |
| NVDA YoY deceleration QoQ (pts) | -13.00 |
| Days since fundamentals anchor quarter-end | - |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.46 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24688 | total=25393 new_days=1 src=yfinance |
| fred | ok_stale | 0 | no fresh pulls succeeded |
| capex | ok | 6 | total=6 latest_period=2025Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  30 |  0.2732 |      0.333 |
| AI_complex_dir_5d | p_constant |  30 |  0.25   |      0.333 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*