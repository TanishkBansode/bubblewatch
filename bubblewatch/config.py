from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LAKE_DIR = DATA_DIR / "lake"
MANUAL_DIR = DATA_DIR / "manual"
LOGS_DIR = BASE_DIR / "logs"
LEDGER_PATH = DATA_DIR / "predictions.jsonl"

# v1: trading-day calendar (no BTC weekend rows), proximity-to-highs sign fix,
# live-feature predictions, NaN-safe targets, trading-day ledger scoring.
MODEL_VERSION = "v1"

RUN_DATE_FMT = "%Y-%m-%d"

TICKER_BUCKETS = {
    "ai_complex": [
        "NVDA", "AVGO", "AMD", "TSM", "MSFT", "GOOGL", "META", "AMZN",
        "AAPL", "ORCL", "CRM", "NOW", "PLTR", "SMCI", "ANET", "MRVL",
        "VRT", "ETN", "PWR", "DLR", "EQIX", "MU",
    ],
    "power_theme": ["CEG", "VST", "NEE", "TLN"],
    "benchmarks": ["SPY", "RSP", "QQQ", "^SOX", "^VIX", "^TNX", "BTC-USD"],
}
ALL_TICKERS = [t for ts in TICKER_BUCKETS.values() for t in ts]
AI_COMPLEX = TICKER_BUCKETS["ai_complex"]
POWER_THEME = TICKER_BUCKETS["power_theme"]

FRED_SERIES = {
    "hy_oas": "BAMLH0A0HYM2",
    "vix_cls": "VIXCLS",
}
FRED_START = "2024-01-01"
FRED_TIMEOUT_S = 45
FRED_RETRIES = 3
# Days after which a source is flagged stale on the dashboard.
STALE_DAYS = {"market": 5, "credit": 7, "fundamentals": 140}

CAPEX_MANUAL_CSV = MANUAL_DIR / "hyperscaler_capex.csv"
CAPEX_SCHEMA = {
    "period": "string",
    "hyperscaler_capex_usd_b": "float64",
    "nvda_rev_yoy_pct": "float64",
}

TEMP_WEIGHTS = {
    "z_mom_stretch": 0.20,
    "z_rs_eqw": 0.15,
    "z_concentration": 0.15,
    "z_credit_tightness": 0.20,
    "z_dd_proximity": 0.20,
    "z_btc_risk": 0.10,
}

# Plain-English metadata for each temperature gauge. `source` is the raw feature the
# z-score is computed from; `sign` is +1 if a higher raw value means hotter.
GAUGES = [
    {"key": "z_mom_stretch", "name": "Price momentum", "source": "ai_mom_60d", "sign": 1,
     "question": "Are AI stocks rising unusually fast?"},
    {"key": "z_credit_tightness", "name": "Credit complacency", "source": "hy_oas", "sign": -1,
     "question": "Are lenders asking for unusually little extra pay to lend to risky companies?"},
    {"key": "z_dd_proximity", "name": "Closeness to the peak", "source": "ai_drawdown_250d", "sign": 1,
     "question": "Are AI stocks sitting unusually close to their 1-year high?"},
    {"key": "z_rs_eqw", "name": "Crowding into AI", "source": "rs_ai_rsp_60d", "sign": 1,
     "question": "Are AI stocks beating the average company by an unusual margin?"},
    {"key": "z_concentration", "name": "Market concentration", "source": "rs_spy_rsp_60d", "sign": 1,
     "question": "Are the giant companies pulling away from everyone else?"},
    {"key": "z_btc_risk", "name": "Risk appetite", "source": "btc_mom_30d", "sign": 1,
     "question": "Are investors unusually eager to gamble (is Bitcoin ripping)?"},
]
GAUGE_KEYS = [g["key"] for g in GAUGES]

SANITY_PCT_LIMIT = 35.0
MARKET_BACKFILL_DAYS = 750
