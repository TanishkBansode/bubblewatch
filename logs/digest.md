# BubbleWatch Daily Digest — 2026-08-23 17:15 UTC

## Verdict
- **Bubble temperature:** **54/100** (warm) — gauge coverage 100%
- **Regime:** `expansion` — uptrend intact without froth extremes
- **Model** P(AI complex up next 5d): **41%** (test Brier 0.2942 vs majority acc 0.639, asof 2026-08-23)

## Key indicators
| Indicator | Value |
|---|---|
| Bubble temperature (0-100) | 54.50 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | 0.05 |
| AI complex momentum 60d | 0.08 |
| Drawdown from 250d high | -0.04 |
| AI complex vs SPY 60d excess | 0.04 |
| AI complex vs equal-weight S&P 60d | 0.03 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.01 |
| Power/utilities theme momentum 60d | -0.10 |
| BTC momentum 30d (risk appetite) | 0.21 |
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
| AI_complex_dir_5d | 5d | 0.41 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| webgen | error | 0 | FileNotFoundError: [Errno 2] No such file or directory: '/home/tanx/project/bubb |
| equities | ok | 24721 | total=24721 new_days=0 src=yfinance |
| fred | ok_stale | 0 | no fresh pulls succeeded |
| capex | ok | 6 | total=6 latest_period=2025Q2 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*