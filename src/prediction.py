"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : CLI Prediction Entry Point
             Run:  python -m src.prediction
"""

import sys

from src.logger import logger
from src.exception import ElectionException
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.components.prediction import KNOWN_STATES


def get_input(prompt: str, cast=str, default=None):
    try:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        return cast(raw)
    except (ValueError, EOFError):
        return default


def main():

    print("\n" + "=" * 60)
    print("   ElectionPulse AI — Election Winner Predictor")
    print("         (Lok Sabha — Classification Model)")
    print("=" * 60)
    print("Enter candidate details. Press ENTER to use defaults.\n")

    try:

        pipeline = PredictionPipeline()

        # -------------------------------------------------------
        # Collect inputs
        # -------------------------------------------------------

        year = get_input("Election Year            [2019] : ", int, 2019)

        print(f"\nKnown states: {', '.join(KNOWN_STATES[:8])} ...")
        state = get_input("\nState Name        [Maharashtra] : ", str, "Maharashtra")

        pc_no = get_input("Constituency No (pc_no)  [24]  : ", int, 24)

        print("\npc_type options: GEN (leave blank), SC, ST")
        pc_type = get_input("Constituency Type      [GEN]  : ", str, "GEN").strip()
        if pc_type not in ["SC", "ST"]:
            pc_type = "Unknown"  # GEN → all OHE zeros = Unknown baseline

        sex = get_input("Candidate Gender (M/F/O)   [M]  : ", str, "M").upper()
        if sex not in ["M", "F", "O"]:
            sex = "M"

        electors = get_input("Total Registered Electors [150000] : ", int, 150000)

        # -------------------------------------------------------
        # Build feature dict
        # -------------------------------------------------------

        candidate = {
            "year":     year,
            "st_name":  state,
            "pc_no":    pc_no,
            "pc_type":  pc_type,
            "cand_sex": sex,
            "electors": electors
        }

        # -------------------------------------------------------
        # Predict
        # -------------------------------------------------------

        result = pipeline.predict_single(candidate)

        # -------------------------------------------------------
        # Display Result
        # -------------------------------------------------------

        print("\n" + "=" * 60)
        print("               PREDICTION RESULT")
        print("=" * 60)
        print(f"  Year              : {year}")
        print(f"  State             : {state}")
        print(f"  Constituency No   : {pc_no}")
        print(f"  Constituency Type : {pc_type}")
        print(f"  Gender            : {sex}")
        print(f"  Electors          : {electors:,}")
        print("-" * 60)
        print(f"  Outcome           : {result['label']}")
        print(f"  Win Probability   : {result['win_prob'] * 100:.2f}%")

        if "predicted_votes" in result:
            print(f"  Estimated Votes   : {result['predicted_votes']:,}")

        print("=" * 60)

        if result["prediction"] == 1:
            print("\n  ✅  This candidate is LIKELY to WIN!\n")
        else:
            print("\n  ❌  This candidate is UNLIKELY to win.\n")

    except Exception as e:
        logger.error(ElectionException(e, sys))
        print(f"\nError : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
