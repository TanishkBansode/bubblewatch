# BubbleWatch Daily Digest — 2026-10-21 05:47 UTC

## Verdict
- **Bubble temperature:** **42/100** (cool) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while still above deep-bear zone
- **Model** P(AI complex up next 5d): **48%** (test Brier 0.2946 vs majority acc 0.548, asof 2026-10-20)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-20 |
| Bubble temperature (0-100) | 42.40 |
| Temperature change vs 1wk ago (pts) | -15.90 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.06 |
| AI complex momentum 60d | 0.10 |
| Drawdown from 250d high | -0.08 |
| AI complex vs SPY 60d excess | 0.07 |
| AI complex vs equal-weight S&P 60d | 0.10 |
| Cap-vs-equal-weight spread 60d (concentration) | 0.04 |
| Power/utilities theme momentum 60d | -0.04 |
| BTC momentum 30d (risk appetite) | 0.04 |
| US HY credit spread OAS (%) | 3.29 |
| HY spread change 5d (pts) | 0.13 |
| Credit spread data as-of | 2026-10-19 |
| VIX close | 17.31 |
| US 10Y yield proxy (%) | 5.12 |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 113 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.48 | 0.50 | logistic on equity+credit features; scored vs constant baseline |

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24721 | total=26093 new_days=1 src=yfinance |
| fred | ok | 24 | total=1457 latest={'hy_oas': '2026-10-19', 'vix_cls': '2026-10-19'} |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  59 |  0.2835 |      0.339 |
| AI_complex_dir_5d | p_constant |  59 |  0.25   |      0.441 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*