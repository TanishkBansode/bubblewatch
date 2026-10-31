import unittest
import numpy as np
import pandas as pd

from bubblewatch import config, features, lppls_model, models, regime, storage


class TestBubbleWatchFeatures(unittest.TestCase):
    def setUp(self):
        dates = pd.date_range("2024-01-01", periods=150, freq="B")
        np.random.seed(42)
        # Synthetic close prices for NVDA and SPY
        p_nvda = 100.0 * np.cumprod(1.0 + np.random.normal(0.001, 0.02, size=len(dates)))
        p_spy = 400.0 * np.cumprod(1.0 + np.random.normal(0.0005, 0.01, size=len(dates)))

        rows = []
        for d, v in zip(dates, p_nvda):
            rows.append({"date": d.strftime("%Y-%m-%d"), "symbol": "NVDA", "close": v})
        for d, v in zip(dates, p_spy):
            rows.append({"date": d.strftime("%Y-%m-%d"), "symbol": "SPY", "close": v})
        self.market_df = pd.DataFrame(rows)

    def test_basket_index(self):
        closes = self.market_df.pivot_table(index="date", columns="symbol", values="close", aggfunc="last")
        rets = closes.pct_change()
        idx = features.basket_index(rets, ["NVDA"])
        self.assertIsInstance(idx, pd.Series)
        valid = idx.dropna()
        self.assertFalse(valid.empty)
        expected_first = 1.0 + rets["NVDA"].dropna().iloc[0]
        self.assertAlmostEqual(valid.iloc[0], expected_first, places=4)

    def test_market_closes(self):
        closes = features.market_closes(self.market_df)
        self.assertIn("NVDA", closes.columns)
        self.assertIn("SPY", closes.columns)
        self.assertEqual(len(closes), 150)

    def test_roll_z(self):
        s = pd.Series(np.linspace(10, 20, 120))
        df = pd.DataFrame({"val": s})
        z = features._roll_z(df, "val", window=100, min_periods=50)
        self.assertTrue(pd.isna(z.iloc[0]))
        self.assertFalse(pd.isna(z.iloc[-1]))
        # The last value in an increasing series should have a positive z-score
        self.assertGreater(z.iloc[-1], 0)

    def test_add_temperature_bounds(self):
        dates = pd.date_range("2024-01-01", periods=120, freq="B")
        df = pd.DataFrame(index=dates)
        for g in config.GAUGES:
            df[g["source"]] = np.random.normal(0.0, 1.0, size=len(dates))

        res = features.add_temperature(df)
        self.assertIn("temperature", res.columns)
        valid_temps = res["temperature"].dropna()
        self.assertTrue((valid_temps >= 0.0).all())
        self.assertTrue((valid_temps <= 100.0).all())

    def test_classify_regime(self):
        snap_expansion = {"ai_drawdown_250d": -0.05, "ai_mom_20d": 0.05, "ai_mom_60d": 0.10, "temperature": 55.0}
        reg, _ = features.classify_regime(snap_expansion)
        self.assertEqual(reg, "expansion")

        snap_contraction = {"ai_drawdown_250d": -0.28, "ai_mom_20d": -0.05, "ai_mom_60d": -0.15, "temperature": 30.0}
        reg, _ = features.classify_regime(snap_contraction)
        self.assertEqual(reg, "contraction")

        snap_hmm_stress = {"ai_drawdown_250d": -0.10, "ai_mom_20d": 0.01, "ai_mom_60d": 0.02, "p_stress": 0.95}
        reg, _ = features.classify_regime(snap_hmm_stress)
        self.assertEqual(reg, "distribution")


class TestHMMRegimeDetector(unittest.TestCase):
    def test_regime_detector_fit(self):
        np.random.seed(42)
        # 100 calm days, then 100 volatile days
        calm = np.random.normal(0.001, 0.005, 100)
        turb = np.random.normal(-0.002, 0.03, 100)
        rets = pd.Series(np.concatenate([calm, turb]), index=pd.date_range("2024-01-01", periods=200, freq="B"))

        detector = regime.HMMRegimeDetector(n_components=2, n_iter=100, random_state=42)
        detector.fit(rets)
        probs = detector.predict_probabilities(rets)

        self.assertIn("p_expansion", probs.columns)
        self.assertIn("p_stress", probs.columns)
        latest = detector.latest_state(rets)
        self.assertEqual(latest["status"], "ok")
        # In the turbulent period, p_stress should be high
        self.assertGreater(latest["p_stress"], 0.70)
        self.assertEqual(latest["regime_state"], "stress")


class TestLPPLSModel(unittest.TestCase):
    def test_lppls_insufficient_history(self):
        short_idx = pd.Series([100.0, 101.0, 102.0])
        res = lppls_model.compute_lppls_hazard(short_idx)
        self.assertEqual(res["status"], "insufficient_history")
        self.assertEqual(res["confidence"], 0.0)

    def test_lppls_execution(self):
        t = np.arange(120, dtype=float)
        # Smooth synthetic series
        p = 100.0 * np.exp(0.005 * t)
        idx = pd.Series(p, index=pd.date_range("2024-01-01", periods=120, freq="B"))
        res = lppls_model.compute_lppls_hazard(idx, windows=[90, 100], max_searches=5)
        self.assertEqual(res["status"], "ok")
        self.assertIn("confidence", res)
        self.assertTrue(0.0 <= res["confidence"] <= 1.0)


class TestModelsAndCalibration(unittest.TestCase):
    def test_brier_decomposition(self):
        y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 1])
        y_prob = np.array([0.7, 0.3, 0.8, 0.6, 0.4, 0.65, 0.35, 0.2, 0.75, 0.8])
        decomp = models.brier_decomposition(y_true, y_prob, n_bins=5)
        self.assertIn("brier", decomp)
        self.assertIn("uncertainty", decomp)
        self.assertIn("reliability", decomp)
        self.assertIn("resolution", decomp)
        self.assertGreater(decomp["uncertainty"], 0.0)
        self.assertGreaterEqual(decomp["reliability"], 0.0)

    def test_make_supervised_purging(self):
        dates = pd.date_range("2024-01-01", periods=100, freq="B")
        feats = pd.DataFrame({"ai_mom_20d": np.random.randn(100), "ai_mom_60d": np.random.randn(100)}, index=dates)
        idx = pd.Series(np.cumprod(1.0 + np.random.randn(100) * 0.01), index=dates)

        sup = models.make_supervised(feats, idx, horizon_days=5, x_cols=["ai_mom_20d", "ai_mom_60d"])
        # Should drop the trailing 5 rows whose future return is unobservable
        self.assertEqual(len(sup), 95)
        self.assertIn("target", sup.columns)
        self.assertFalse(sup["target"].isna().any())

    def test_direction_predictions_structure(self):
        proxy = {
            "status": "ok",
            "p_ai_up_5d": 0.62,
            "p_ai_up_21d": 0.70,
            "p_tail_down_5pct_21d": 0.09,
            "train_base_rate": 0.60,
            "asof": "2026-10-30",
        }
        preds = models.direction_predictions(proxy)
        self.assertEqual(len(preds), 3)
        targets = [p["target"] for p in preds]
        self.assertIn("AI_complex_dir_5d", targets)
        self.assertIn("AI_complex_dir_21d", targets)
        self.assertIn("AI_complex_tail_21d", targets)


if __name__ == "__main__":
    unittest.main()
