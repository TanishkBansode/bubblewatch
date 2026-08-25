# BubbleWatch Daily Digest — 2026-08-25 02:20 UTC

## Verdict
- **Bubble temperature:** **56/100** (warm) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while still above deep-bear zone
- **Model** P(AI complex up next 5d): **48%** (test Brier 0.2937 vs majority acc 0.628, asof 2026-08-25)

## Key indicators
| Indicator | Value |
|---|---|
| Bubble temperature (0-100) | 56.10 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.01 |
| AI complex momentum 60d | 0.07 |
| Drawdown from 250d high | -0.06 |
| AI complex vs SPY 60d excess | 0.02 |
| AI complex vs equal-weight S&P 60d | 0.02 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.01 |
| Power/utilities theme momentum 60d | -0.11 |
| BTC momentum 30d (risk appetite) | 0.24 |
| US HY credit spread OAS (%) | 2.75 |
| HY spread change 5d (pts) | 0.00 |
| VIX close | 16.01 |
| Hyperscaler capex, latest qtr ($B) | 88.00 |
| Hyperscaler capex YoY (%) | 65.40 |
| NVDA revenue YoY (%) | 56.00 |
| NVDA YoY deceleration QoQ (pts) | -13.00 |
| Days since fundamentals anchor quarter-end | - |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.48 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24720 | total=24755 new_days=1 src=yfinance |
| fred | ok_stale | 0 | no fresh pulls succeeded |
| capex | ok | 6 | total=6 latest_period=2025Q2 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*