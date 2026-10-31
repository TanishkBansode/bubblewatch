from __future__ import annotations

import logging
import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM

logger = logging.getLogger(__name__)


class HMMRegimeDetector:
    """
    Two-state Gaussian Hidden Markov Model for market regime detection.
    State 0: Low-volatility expansion / stable regime
    State 1: High-volatility stress / distribution regime

    Features:
      - 1D daily log-return of the AI complex basket
      - 1D 20-day annualized rolling volatility
    States are deterministically ordered by volatility to eliminate label-switching.
    """

    def __init__(self, n_components: int = 2, n_iter: int = 200, random_state: int = 42):
        self.n_components = n_components
        self.n_iter = n_iter
        self.random_state = random_state
        self.model: GaussianHMM | None = None
        self.state_order_: np.ndarray | None = None

    def _prepare_features(self, returns: pd.Series) -> pd.DataFrame:
        clean_ret = returns.dropna()
        log_ret = np.log1p(clean_ret)
        # 20-day annualized volatility (min 10 days)
        roll_vol = clean_ret.rolling(20, min_periods=10).std() * np.sqrt(252)
        df = pd.DataFrame({"log_ret": log_ret, "vol": roll_vol}, index=clean_ret.index).dropna()
        return df

    def fit(self, returns: pd.Series) -> HMMRegimeDetector:
        df = self._prepare_features(returns)
        if len(df) < 60:
            return self

        X = df[["log_ret", "vol"]].to_numpy()
        hmm = GaussianHMM(
            n_components=self.n_components,
            covariance_type="full",
            n_iter=self.n_iter,
            random_state=self.random_state,
        )
        hmm.fit(X)

        # Sort states by volatility variance: State 0 = lowest vol, State 1 = highest vol
        # Covariance diagonal for feature index 1 ('vol')
        vol_variances = [float(hmm.covars_[i, 1, 1]) for i in range(self.n_components)]
        self.state_order_ = np.argsort(vol_variances)
        self.model = hmm
        return self

    def predict_probabilities(self, returns: pd.Series) -> pd.DataFrame:
        if self.model is None or self.state_order_ is None:
            return pd.DataFrame(columns=["p_expansion", "p_stress"], index=returns.index)

        df = self._prepare_features(returns)
        if df.empty:
            return pd.DataFrame(columns=["p_expansion", "p_stress"], index=returns.index)

        X = df[["log_ret", "vol"]].to_numpy()
        raw_probs = self.model.predict_proba(X)

        # Reorder probabilities according to state_order_
        ordered_probs = raw_probs[:, self.state_order_]
        res = pd.DataFrame(
            {
                "p_expansion": ordered_probs[:, 0],
                "p_stress": ordered_probs[:, 1],
            },
            index=df.index,
        )
        return res.reindex(returns.index).ffill()

    def latest_state(self, returns: pd.Series) -> dict:
        """Return the latest regime state diagnosis with transition metrics."""
        probs = self.predict_probabilities(returns)
        if probs.empty or probs["p_stress"].isna().all():
            return {
                "status": "insufficient_data",
                "p_stress": None,
                "p_expansion": None,
                "regime_state": "unknown",
                "persistence": None,
            }

        latest_stress = float(probs["p_stress"].iloc[-1])
        latest_exp = float(probs["p_expansion"].iloc[-1])

        state_label = "stress" if latest_stress >= 0.50 else "expansion"

        persistence = None
        if self.model is not None and self.state_order_ is not None:
            # Transition matrix re-ordered
            tm = self.model.transmat_[self.state_order_][:, self.state_order_]
            curr_idx = 1 if state_label == "stress" else 0
            persistence = float(tm[curr_idx, curr_idx])

        return {
            "status": "ok",
            "p_stress": round(latest_stress, 3),
            "p_expansion": round(latest_exp, 3),
            "regime_state": state_label,
            "persistence": round(persistence, 3) if persistence is not None else None,
        }


def detect_ai_regime(returns: pd.Series) -> dict:
    """Convenience functional interface to train and diagnose AI complex regime."""
    detector = HMMRegimeDetector()
    detector.fit(returns)
    return detector.latest_state(returns)

