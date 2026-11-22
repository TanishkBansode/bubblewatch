# BubbleWatch Daily Digest — 2026-11-22 07:51 UTC

## Verdict
- **Bubble temperature:** **4/100** (frost) — gauge coverage 100%
- **Regime:** `contraction` — AI complex in deep drawdown (-27%) (HMM stress 100%)
- **Model** P(AI complex up next 5d): **75%** (test Brier 0.2731 vs majority acc 0.533, asof 2026-11-20)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-11-20 |
| Bubble temperature (0-100) | 3.90 |
| Temperature change vs 1wk ago (pts) | -14.40 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.18 |
| AI complex momentum 60d | -0.22 |
| Drawdown from 250d high | -0.27 |
| AI complex breadth (% positive 20d) | 0.09 |
| AI complex 20d return dispersion | 0.15 |
| AI complex vs SPY 60d excess | -0.12 |
| AI complex vs equal-weight S&P 60d | -0.17 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.04 |
| Power/utilities theme momentum 60d | -0.06 |
| BTC momentum 30d (risk appetite) | -0.29 |
| US HY credit spread OAS (%) | 3.52 |
| HY spread change 5d (pts) | 0.29 |
| Credit spread data as-of | 2026-11-19 |
| VIX close | 35.89 |
| VIX vs 20d MA ratio (term proxy) | 0.65 |
| US 10Y yield proxy (%) | 4.91 |
| US 10Y TIPS real yield (%) | 2.88 |
| US 10Y-2Y yield curve spread (%) | 0.29 |
| HMM turbulence probability (P_stress) | 1.00 |
| LPPLS bubble singularity confidence | 0.00 |
| LPPLS projected trading days to t_c | - |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 145 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.75 | 0.50 | regularized logistic on equity+credit+breadth; purged train/test |
| AI_complex_dir_21d | 21d | 0.80 | 0.50 | 21-trading-day direction forecast (~1 month) |
| AI_complex_tail_21d | 21d | 0.03 | 0.15 | 21-trading-day tail risk hazard: P(return <= -5%) |

## Alerts
- ⚠️ Ice zone (4/100): extreme pessimism often marks late-stage selloffs
- ⚠️ AI complex drawdown -27% from highs
- ⚠️ Fundamentals anchor stale (latest quarter 2026Q2, 145d old) — append new quarters to data/manual/hyperscaler_capex.csv
- ⚠️ HMM statistical regime detects elevated volatility turbulence (P_stress = 100%)

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24724 | total=26861 new_days=1 src=yfinance |
| fred | ok | 42 | total=2946 latest={'hy_oas': '2026-11-19', 'real_yield_10y': '2026-11-19', 'vix_ |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  92 |  0.2944 |      0.272 |
| AI_complex_dir_5d | p_constant |  92 |  0.25   |      0.554 |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*