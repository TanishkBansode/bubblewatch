# BubbleWatch Daily Digest — 2026-09-05 05:23 UTC

## Verdict
- **Bubble temperature:** **54/100** (warm) — gauge coverage 80%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **46%** (test Brier 0.2987 vs majority acc 0.662, asof 2026-08-25)

## Key indicators
| Indicator | Value |
|---|---|
| Bubble temperature (0-100) | 54.40 |
| Gauge coverage | 0.80 |
| AI complex momentum 20d | 0.01 |
| AI complex momentum 60d | 0.12 |
| Drawdown from 250d high | -0.01 |
| AI complex vs SPY 60d excess | 0.09 |
| AI complex vs equal-weight S&P 60d | 0.10 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.01 |
| Power/utilities theme momentum 60d | -0.00 |
| BTC momentum 30d (risk appetite) | 0.24 |
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
| equities | ok | 24720 | total=25054 new_days=1 src=yfinance |
| fred | ok_stale | 0 | no fresh pulls succeeded |
| capex | ok | 6 | total=6 latest_period=2025Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  12 |  0.2978 |      0.167 |
| AI_complex_dir_5d | p_constant |  12 |  0.25   |      0.167 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*