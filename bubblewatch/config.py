from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LAKE_DIR = DATA_DIR / "lake"
MANUAL_DIR = DATA_DIR / "manual"
LOGS_DIR = BASE_DIR / "logs"
LEDGER_PATH = DATA_DIR / "predictions.jsonl"

MODEL_VERSION = "v0"

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

SANITY_PCT_LIMIT = 35.0
MARKET_BACKFILL_DAYS = 750
