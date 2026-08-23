# BubbleWatch

Daily AI-bubble thermometer. Watches the AI equity complex, credit spreads, crowding and
concentration signals; publishes a 0–100 **Bubble Temperature**, a regime classification and a
self-scored direction forecast to GitHub Pages every morning.

**Live site:** https://tanishkbansode.github.io/bubblewatch/

## What it does

1. Ingests daily: 22-name AI complex + power/utilities + benchmarks (Yahoo → Stooq fallback),
   FRED high-yield OAS & VIX (keyless CSV), quarterly hyperscaler capex / NVDA YoY (manual seed).
2. Computes six z-scored gauges → weighted **Bubble Temperature** → regime
   (`expansion / euphoria / distribution / contraction / capitulation_recovery`).
3. Trains a logistic P(AI complex up next 5d) on chronological splits, logs predictions to an
   append-only ledger, scores them against a permanent constant-0.50 baseline once horizons elapse.
4. Renders `web/` (dashboard + three explainer pages), commits fresh data as `bubblewatch-bot`,
   deploys via GitHub Pages.

## Local run

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m bubblewatch.pipeline run     # ingest + features + models + digest + web
python -m bubblewatch.pipeline report  # rebuild digest/site from existing lake
python -m bubblewatch.pipeline eval    # print prediction scoreboard
```

Outputs: `logs/digest.md`, `web/index.html` (+ explainer pages), lake parquet in `data/lake/`.

## Quarterly maintenance

Append one row to `data/manual/hyperscaler_capex.csv` after each earnings season:

```
2025Q3,<combined MSFT+GOOGL+AMZN+META capex $B>,<NVDA revenue YoY %>
```

The dashboard surfaces staleness automatically.

## Ops notes

- Schedule: daily 01:00 UTC (+ manual dispatch). The bot commits `data logs web` — always
  `git pull --rebase` before pushing local changes.
- Seed values through 2025Q2 are approximate from earnings releases; verify before trusting.
- Not investment advice. See `templates/guide.html` for the exact temperature formula.
