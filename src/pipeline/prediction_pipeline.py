"""
Author      : Kavya Parnami
Project     : ElectionPulse AI
Description : Prediction Pipeline
"""

import sys
import pandas as pd

from src.logger import logger
from src.exception import ElectionException
from src.components.prediction import PredictionHelper
from src.data.election_knowledge import get_party_win_probability


class PredictionPipeline:
    """
    High-level wrapper around PredictionHelper.

    Input features (all raw — no pre-encoding needed):
        year, st_name, pc_no, pc_type, cand_sex, electors
    """

    def __init__(self):
        logger.info("Initialising Prediction Pipeline")
        self.helper = PredictionHelper()
        logger.info("Prediction Pipeline Ready")

    # ----------------------------------------------------------
    # predict_single
    # ----------------------------------------------------------

    def predict_single(self, candidate_features: dict) -> dict:
        """Predict win/loss for a single candidate."""

        try:

            result_df = self.helper.predict(candidate_features)

            prediction = int(result_df["prediction"].iloc[0])
            win_prob   = float(result_df["win_prob"].iloc[0])

            output = {
                "prediction": prediction,
                "win_prob":   win_prob,
                "label":      "WINNER" if prediction == 1 else "NOT WINNER"
            }

            # Add vote estimate if regressor available
            if self.helper.regressor is not None:
                votes = self.helper.predict_votes(candidate_features)
                output["predicted_votes"] = int(votes["predicted_votes"].iloc[0])

            return output

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)

    # ----------------------------------------------------------
    # predict_party_contest
    # ----------------------------------------------------------

    def predict_party_contest(self, contest_data: dict) -> dict:
        """
        Predict head-to-head party winner in a Lok Sabha constituency.

        Uses:
          1. 2024 + 2019 constituency-level historical winner (primary signal)
          2. 2024 + 2019 state-level seat share (secondary signal)
          3. ML model's generic win_prob as a minor adjustment
        """
        try:
            st_name       = contest_data.get("st_name", "Maharashtra")
            pc_no         = int(contest_data.get("pc_no", 24))
            year          = int(contest_data.get("year", 2029))
            pc_type       = contest_data.get("pc_type", "GEN")
            constituency  = contest_data.get("constituency_name") or ""
            electors      = int(contest_data.get("electors", 150000))
            party1        = contest_data.get("party1", "BJP")
            party2        = contest_data.get("party2", "Congress")

            # ── Historical knowledge base (2024 + 2019 data) ────────────
            hist_prob1, hist_prob2 = get_party_win_probability(
                party1, party2, st_name, constituency
            )

            # ── ML model win_prob as minor signal (generic tendency) ────
            cand_base = {
                "year":     year,
                "st_name":  st_name,
                "pc_no":    pc_no,
                "pc_type":  pc_type,
                "cand_sex": "M",
                "electors": electors,
            }
            try:
                ml_res = self.predict_single(cand_base)
                ml_win_prob = ml_res.get("win_prob", 0.5)
            except Exception:
                ml_win_prob = 0.5

            # ── Blend: 85% historical knowledge + 15% ML generic signal ─
            # The ML signal only nudges, never overrides the historical data
            ml_delta = (ml_win_prob - 0.5) * 0.15
            raw1 = hist_prob1 + ml_delta
            raw2 = hist_prob2 - ml_delta
            tot  = raw1 + raw2 if (raw1 + raw2) > 0 else 1.0

            prob1 = round(max(0.02, min(0.98, raw1 / tot)), 4)
            prob2 = round(1.0 - prob1, 4)

            # ── Vote estimate ───────────────────────────────────────────
            base_votes = int(electors * 0.60)  # avg ~60% turnout
            votes1 = int(base_votes * prob1 * 1.1)
            votes2 = int(base_votes * prob2 * 1.1)

            winner     = party1 if prob1 >= prob2 else party2
            confidence = max(prob1, prob2)

            return {
                "state":             st_name,
                "constituency_name": constituency or f"Constituency #{pc_no}",
                "pc_no":             pc_no,
                "year":              year,
                "winner":            winner,
                "confidence":        confidence,
                "data_source":       "2024+2019 election results",
                "party1": {
                    "name":            party1,
                    "win_prob":        prob1,
                    "predicted_votes": votes1
                },
                "party2": {
                    "name":            party2,
                    "win_prob":        prob2,
                    "predicted_votes": votes2
                },
            }

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)

    # ----------------------------------------------------------
    # predict_constituency
    # ----------------------------------------------------------

    def predict_constituency(self, candidates: list[dict]) -> dict:
        """
        Given all candidates in a constituency, predict the winner.
        """

        try:
            return self.helper.predict_winner(candidates)

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)

    # ----------------------------------------------------------
    # predict_batch
    # ----------------------------------------------------------

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Batch prediction — returns df with prediction + win_prob appended."""

        try:

            result_df = self.helper.predict(df)

            output = df.copy()
            output["prediction"] = result_df["prediction"].values
            output["win_prob"]   = result_df["win_prob"].values
            output["label"]      = output["prediction"].map({1: "WINNER", 0: "NOT WINNER"})

            return output

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    pipeline = PredictionPipeline()

    # Single candidate
    sample = {
        "year":     2019,
        "st_name":  "Maharashtra",
        "pc_no":    24,
        "pc_type":  "GEN",
        "cand_sex": "M",
        "electors": 200000
    }

    result = pipeline.predict_single(sample)

    print("=" * 60)
    print("SINGLE CANDIDATE PREDICTION")
    print("=" * 60)
    print(f"Prediction    : {result['label']}")
    print(f"Win Prob      : {result['win_prob'] * 100:.2f}%")
    if "predicted_votes" in result:
        print(f"Est Votes     : {result['predicted_votes']:,}")

    # Constituency winner
    constituency = [
        {"year": 2019, "st_name": "Maharashtra", "pc_no": 24,
         "pc_type": "GEN", "cand_sex": "M", "electors": 200000},
        {"year": 2019, "st_name": "Maharashtra", "pc_no": 24,
         "pc_type": "GEN", "cand_sex": "F", "electors": 200000},
        {"year": 2019, "st_name": "Maharashtra", "pc_no": 24,
         "pc_type": "GEN", "cand_sex": "M", "electors": 200000},
    ]

    winner = pipeline.predict_constituency(constituency)

    print("\n" + "=" * 60)
    print("CONSTITUENCY WINNER")
    print("=" * 60)
    print(f"Winner Index  : {winner['winner_index']}")
    print(f"Win Prob      : {winner['win_prob'] * 100:.2f}%")
    print(winner["all_results"])
