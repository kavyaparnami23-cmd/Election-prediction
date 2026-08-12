"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Prediction Helper Component
             Works with already-trained models in artifacts/models/
"""

import os
import sys
import pandas as pd
import numpy as np

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


# ================================================================
# Known states used during training (for OHE alignment)
# ================================================================

KNOWN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chandigarh", "Chattisgarh", "Chhattisgarh",
    "Dadra & Nagar Haveli", "Daman & Diu", "Delhi", "Goa",
    "Goa Daman & Diu", "Goa, Daman & Diu", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jammu & Kashmir", "Jharkhand",
    "Karnataka", "Kerala", "Lakshadweep", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "National Capital Territory Of Delhi", "Nct Of Delhi",
    "Odisha", "Orissa", "Pondicherry", "Puducherry", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "Uttaranchal", "West Bengal"
]

KNOWN_PC_TYPES = ["SC", "SC ", "ST", "Unknown"]
KNOWN_SEX      = ["M", "O", "Unknown"]


class PredictionHelper:
    """
    Loads the pre-trained RandomForestClassifier (best_model.pkl)
    and XGBRegressor (regression_model.pkl) from artifacts/models/.

    The models were trained on ONE-HOT-ENCODED Lok Sabha data.
    This class handles the OHE transformation at inference time.

    Input features (raw / human-readable):
        - year       : int   e.g. 2019
        - st_name    : str   e.g. "Maharashtra"
        - pc_no      : int   e.g. 24
        - pc_type    : str   "GEN" | "SC" | "ST"  (default "Unknown")
        - cand_sex   : str   "M" | "F" | "O"      (default "M")
        - electors   : int   e.g. 150000
    """

    def __init__(self):

        classifier_path = os.path.join(Config.MODEL_DIR, "best_model.pkl")
        regressor_path  = os.path.join(Config.MODEL_DIR, "regression_model.pkl")

        if not os.path.exists(classifier_path):
            raise FileNotFoundError(
                f"Trained classifier not found : {classifier_path}\n"
                "Please run the training pipeline first."
            )

        logger.info(f"Loading classifier  : {classifier_path}")
        self.classifier = Utils.load_object(classifier_path)

        if os.path.exists(regressor_path):
            logger.info(f"Loading regressor   : {regressor_path}")
            self.regressor = Utils.load_object(regressor_path)
        else:
            self.regressor = None
            logger.warning("regression_model.pkl not found — vote prediction disabled")

        logger.info("Models loaded successfully")

    # ----------------------------------------------------------
    # Internal: build the OHE feature row the model expects
    # ----------------------------------------------------------

    def _encode(self, raw: dict) -> pd.DataFrame:
        """
        Convert a raw candidate dict into the 52-column OHE
        DataFrame that best_model.pkl / regression_model.pkl expect.
        """

        year     = int(raw.get("year", 2019))
        pc_no    = int(raw.get("pc_no", 1))
        electors = int(raw.get("electors", 100000))
        st_name  = str(raw.get("st_name", "Unknown"))
        pc_type  = str(raw.get("pc_type", "Unknown"))
        cand_sex = str(raw.get("cand_sex", "M"))

        row = {"year": year, "pc_no": pc_no, "electors": electors}

        # OHE state
        for s in KNOWN_STATES:
            row[f"st_name_{s}"] = int(st_name == s)

        # OHE pc_type
        for t in KNOWN_PC_TYPES:
            row[f"pc_type_{t}"] = int(pc_type == t)

        # OHE cand_sex  (Female = all zeros — baseline)
        for g in KNOWN_SEX:
            row[f"cand_sex_{g}"] = int(cand_sex == g)

        return pd.DataFrame([row])

    # ----------------------------------------------------------
    # predict : winner classification
    # ----------------------------------------------------------

    def predict(self, input_data: dict | pd.DataFrame) -> pd.DataFrame:
        """
        Parameters
        ----------
        input_data : dict or pd.DataFrame of raw candidate features

        Returns
        -------
        pd.DataFrame with columns:
            - prediction  : 0 (Not Winner) or 1 (Winner)
            - win_prob    : probability of winning (0–1)
        """

        try:

            if isinstance(input_data, dict):
                records = [input_data]
            elif isinstance(input_data, list):
                records = input_data
            else:
                records = input_data.to_dict(orient="records")

            encoded_rows = pd.concat(
                [self._encode(r) for r in records],
                ignore_index=True
            )

            logger.info(f"Predicting for {len(records)} candidate(s)")

            preds = self.classifier.predict(encoded_rows)
            proba = self.classifier.predict_proba(encoded_rows)[:, 1]

            result = pd.DataFrame({
                "prediction": preds,
                "win_prob":   proba.round(4)
            })

            return result

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)

    # ----------------------------------------------------------
    # predict_votes : regression — estimated vote count
    # ----------------------------------------------------------

    def predict_votes(self, input_data: dict | pd.DataFrame) -> pd.DataFrame:
        """
        Predict estimated total votes polled using the XGBRegressor.
        """

        try:

            if self.regressor is None:
                raise RuntimeError("Regression model not loaded")

            if isinstance(input_data, dict):
                records = [input_data]
            else:
                records = input_data.to_dict(orient="records")

            encoded_rows = pd.concat(
                [self._encode(r) for r in records],
                ignore_index=True
            )

            votes = self.regressor.predict(encoded_rows)

            return pd.DataFrame({
                "predicted_votes": np.maximum(votes, 0).round(0).astype(int)
            })

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)

    # ----------------------------------------------------------
    # predict_winner : pick winner from a list of candidates
    # ----------------------------------------------------------

    def predict_winner(self, candidates: list[dict]) -> dict:
        """
        Given all candidates in one constituency, return the
        predicted winner (highest win probability).
        """

        try:

            result_df = self.predict(candidates)

            winner_idx  = result_df["win_prob"].idxmax()
            winner_prob = float(result_df.loc[winner_idx, "win_prob"])

            logger.info(f"Predicted winner index={winner_idx}, prob={winner_prob:.4f}")

            return {
                "winner_index": int(winner_idx),
                "winner_data":  candidates[winner_idx],
                "win_prob":     winner_prob,
                "all_results":  result_df
            }

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    helper = PredictionHelper()

    sample = {
        "year":     2019,
        "st_name":  "Rajasthan",
        "pc_no":    5,
        "pc_type":  "GEN",
        "cand_sex": "M",
        "electors": 150000
    }

    result = helper.predict(sample)

    print("=" * 60)
    print("PREDICTION RESULT")
    print("=" * 60)
    print(f"Outcome  : {'WINNER' if result['prediction'][0] == 1 else 'NOT WINNER'}")
    print(f"Win Prob : {result['win_prob'][0] * 100:.2f}%")

    if helper.regressor:
        votes = helper.predict_votes(sample)
        print(f"Est Votes: {votes['predicted_votes'][0]:,}")
