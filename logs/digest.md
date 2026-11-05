# BubbleWatch Daily Digest — 2026-11-05 07:47 UTC

## Verdict
- **Bubble temperature:** **16/100** (frost) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while above deep-bear zone (HMM stress 100%)
- **Model** P(AI complex up next 5d): **64%** (test Brier 0.2439 vs majority acc 0.588, asof 2026-11-04)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-11-04 |
| Bubble temperature (0-100) | 16.30 |
| Temperature change vs 1wk ago (pts) | -27.00 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.14 |
| AI complex momentum 60d | -0.06 |
| Drawdown from 250d high | -0.14 |
| AI complex breadth (% positive 20d) | 0.27 |
| AI complex 20d return dispersion | 0.13 |
| AI complex vs SPY 60d excess | -0.05 |
| AI complex vs equal-weight S&P 60d | -0.06 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.02 |
| Power/utilities theme momentum 60d | -0.08 |
| BTC momentum 30d (risk appetite) | -0.05 |
| US HY credit spread OAS (%) | 3.40 |
| HY spread change 5d (pts) | 0.26 |
| Credit spread data as-of | 2026-11-03 |
| VIX close | 16.61 |
| US 10Y yield proxy (%) | 4.89 |
| US 10Y TIPS real yield (%) | 2.65 |
| US 10Y-2Y yield curve spread (%) | 0.32 |
| HMM turbulence probability (P_stress) | 1.00 |
| LPPLS bubble singularity confidence | 0.00 |
| LPPLS projected trading days to t_c | - |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 128 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.64 | 0.50 | regularized logistic on equity+credit+breadth; purged train/test |
| AI_complex_dir_21d | 21d | 0.53 | 0.50 | 21-trading-day direction forecast (~1 month) |
| AI_complex_tail_21d | 21d | 0.24 | 0.15 | 21-trading-day tail risk hazard: P(return <= -5%) |

## Alerts
- ⚠️ Ice zone (16/100): extreme pessimism often marks late-stage selloffs
- ⚠️ HMM statistical regime detects elevated volatility turbulence (P_stress = 100%)

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24722 | total=26460 new_days=1 src=yfinance |
| fred | ok | 48 | total=2900 latest={'hy_oas': '2026-11-03', 'real_yield_10y': '2026-11-03', 'vix_ |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  74 |  0.2902 |      0.27  |
| AI_complex_dir_5d | p_constant |  74 |  0.25   |      0.514 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*