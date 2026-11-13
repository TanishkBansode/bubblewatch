# BubbleWatch Daily Digest — 2026-11-13 07:40 UTC

## Verdict
- **Bubble temperature:** **21/100** (frost) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while above deep-bear zone (HMM stress 100%)
- **Model** P(AI complex up next 5d): **54%** (test Brier 0.2494 vs majority acc 0.564, asof 2026-11-12)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-11-12 |
| Bubble temperature (0-100) | 21.30 |
| Temperature change vs 1wk ago (pts) | 13.20 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.07 |
| AI complex momentum 60d | -0.04 |
| Drawdown from 250d high | -0.13 |
| AI complex breadth (% positive 20d) | 0.32 |
| AI complex 20d return dispersion | 0.13 |
| AI complex vs SPY 60d excess | -0.02 |
| AI complex vs equal-weight S&P 60d | -0.02 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.01 |
| Power/utilities theme momentum 60d | 0.05 |
| BTC momentum 30d (risk appetite) | -0.16 |
| US HY credit spread OAS (%) | 3.30 |
| HY spread change 5d (pts) | -0.18 |
| Credit spread data as-of | 2026-11-11 |
| VIX close | 18.70 |
| US 10Y yield proxy (%) | 5.10 |
| US 10Y TIPS real yield (%) | 2.78 |
| US 10Y-2Y yield curve spread (%) | 0.24 |
| HMM turbulence probability (P_stress) | 1.00 |
| LPPLS bubble singularity confidence | 0.00 |
| LPPLS projected trading days to t_c | - |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 136 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.54 | 0.50 | regularized logistic on equity+credit+breadth; purged train/test |
| AI_complex_dir_21d | 21d | 0.57 | 0.50 | 21-trading-day direction forecast (~1 month) |
| AI_complex_tail_21d | 21d | 0.30 | 0.15 | 21-trading-day tail risk hazard: P(return <= -5%) |

## Alerts
- ⚠️ Ice zone (21/100): extreme pessimism often marks late-stage selloffs
- ⚠️ HMM statistical regime detects elevated volatility turbulence (P_stress = 100%)

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 23973 | total=26659 new_days=1 src=yfinance |
| fred | ok | 48 | total=2921 latest={'hy_oas': '2026-11-11', 'real_yield_10y': '2026-11-10', 'vix_ |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  84 |  0.2973 |      0.262 |
| AI_complex_dir_5d | p_constant |  84 |  0.25   |      0.548 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*