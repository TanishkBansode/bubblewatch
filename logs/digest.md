# BubbleWatch Daily Digest — 2026-11-03 07:41 UTC

## Verdict
- **Bubble temperature:** **13/100** (frost) — gauge coverage 100%
- **Regime:** `distribution` — short-term momentum rolled over while above deep-bear zone (HMM stress 100%)
- **Model** P(AI complex up next 5d): **66%** (test Brier 0.2404 vs majority acc 0.599, asof 2026-11-02)

## Key indicators
| Indicator | Value |
|---|---|
| Market data as-of | 2026-11-02 |
| Bubble temperature (0-100) | 13.30 |
| Temperature change vs 1wk ago (pts) | -22.50 |
| Gauge coverage | 1.00 |
| AI complex momentum 20d | -0.14 |
| AI complex momentum 60d | -0.07 |
| Drawdown from 250d high | -0.15 |
| AI complex breadth (% positive 20d) | 0.05 |
| AI complex 20d return dispersion | 0.10 |
| AI complex vs SPY 60d excess | -0.03 |
| AI complex vs equal-weight S&P 60d | -0.06 |
| Cap-vs-equal-weight spread 60d (concentration) | -0.03 |
| Power/utilities theme momentum 60d | -0.02 |
| BTC momentum 30d (risk appetite) | -0.11 |
| US HY credit spread OAS (%) | 3.44 |
| HY spread change 5d (pts) | 0.14 |
| Credit spread data as-of | 2026-10-30 |
| VIX close | 21.15 |
| US 10Y yield proxy (%) | 4.89 |
| US 10Y TIPS real yield (%) | 2.60 |
| US 10Y-2Y yield curve spread (%) | 0.32 |
| HMM turbulence probability (P_stress) | 1.00 |
| LPPLS bubble singularity confidence | 0.00 |
| LPPLS projected trading days to t_c | - |
| Hyperscaler capex, latest qtr ($B) | 166.60 |
| Hyperscaler capex YoY (%) | 89.30 |
| NVDA revenue YoY (%) | 106.00 |
| NVDA YoY deceleration QoQ (pts) | 21.00 |
| Fundamentals anchor quarter | 2026Q2 |
| Days since fundamentals quarter-end | 126 |

## Today's predictions (logged to ledger)
| Target | Horizon | Model P(up) | Constant baseline | Note |
|---|---|---|---|---|
| AI_complex_dir_5d | 5d | 0.66 | 0.50 | regularized logistic on equity+credit+breadth; purged train/test |
| AI_complex_dir_21d | 21d | 0.69 | 0.50 | 21-trading-day direction forecast (~1 month) |
| AI_complex_tail_21d | 21d | 0.14 | 0.15 | 21-trading-day tail risk hazard: P(return <= -5%) |

## Alerts
- ⚠️ Ice zone (13/100): extreme pessimism often marks late-stage selloffs
- ⚠️ HMM statistical regime detects elevated volatility turbulence (P_stress = 100%)

## Source status (this run)
| Source | Status | Rows | Detail |
|---|---|---|---|
| equities | ok | 24722 | total=26394 new_days=1 src=yfinance |
| fred | ok | 48 | total=2892 latest={'hy_oas': '2026-10-30', 'real_yield_10y': '2026-10-30', 'vix_ |
| capex | ok | 10 | total=10 latest_period=2026Q2 |

## Prediction scoreboard (vs baselines)
| target            | model      |   n |   brier |   accuracy |
|:------------------|:-----------|----:|--------:|-----------:|
| AI_complex_dir_5d | p_model    |  72 |  0.2892 |      0.278 |
| AI_complex_dir_5d | p_constant |  72 |  0.25   |      0.5   |

---
*Temperature = weighted z-composite; formula and weights published on the site. Baselines are permanent. Not investment advice.*