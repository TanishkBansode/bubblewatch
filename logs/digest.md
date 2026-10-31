# BubbleWatch Daily Digest — 2026-10-31 04:49 UTC

## Verdict
- **Bubble temperature:** **35/100** (cool) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while above deep-bear zone (HMM stress 100%)
- **Model** P(AI complex up next 5d): **63%** (test Brier 0.2375 vs majority acc 0.605, asof 2026-10-29)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-10-29 |
| Bubble temperature (0-100) | 35.30 |
| Temperature change vs 1wk ago (pts) | -6.80 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.06 |
| AI complex momentum 60d | 0.02 |
| Drawdown from 250d high | -0.09 |
| AI complex breadth (% positive 20d) | 0.32 |
| AI complex 20d return dispersion | 0.08 |
| AI complex vs SPY 60d excess | 0.02 |
| AI complex vs equal-weight S&P 60d | 0.02 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.00 |
| Power/utilities theme momentum 60d | 0.01 |
| BTC momentum 30d (risk appetite) | 0.04 |
| US HY credit spread OAS (%) | 3.14 |
| HY spread change 5d (pts) | -0.26 |
| Credit spread data as-of | 2026-10-28 |
| VIX close | 17.20 |
| US 10Y yield proxy (%) | 4.99 |
| HMM turbulence probability (P_stress) | 1.00 |
| LPPLS bubble singularity confidence | 0.00 |
| LPPLS projected trading days to t_c | - |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 123 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.63 | 0.50 | regularized logistic on equity+credit+breadth; purged train/test |
| AI_complex_dir_21d | 21d | 0.83 | 0.50 | 21-trading-day direction forecast (~1 month) |
| AI_complex_tail_21d | 21d | 0.07 | 0.15 | 21-trading-day tail risk hazard: P(return <= -5%) |

## Alerts
- ⚠️ HMM statistical regime detects elevated volatility turbulence (P_stress = 100%)

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  68 |  0.2874 |      0.294 |
| AI_complex_dir_5d | p_constant |  68 |  0.25   |      0.471 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*