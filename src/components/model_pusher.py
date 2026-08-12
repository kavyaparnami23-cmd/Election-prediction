"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Model Pusher Component — promotes best model to production
"""

import os
import sys
import shutil
import joblib
from datetime import datetime

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


class ModelPusher:
    """
    Compares the newly trained model against any existing
    production model.  If the new model is better (higher F1),
    it copies the model file to artifacts/models/production/
    and saves a versioned backup.
    """

    # Minimum F1 improvement required to push (0 = always push if better)
    MIN_IMPROVEMENT_THRESHOLD = 0.0

    def initiate_model_pusher(
        self,
        new_model_f1: float,
        new_model_name: str = "best_classifier"
    ):

        try:

            logger.info("=" * 50)
            logger.info("Model Pusher Started")
            logger.info("=" * 50)

            # --------------------------------------------------
            # Paths
            # --------------------------------------------------

            source_path = os.path.join(Config.MODEL_DIR, "best_classifier.pkl")

            prod_dir    = Config.PRODUCTION_MODEL_DIR

            prod_path   = os.path.join(prod_dir, "model.pkl")

            meta_path   = os.path.join(prod_dir, "model_meta.txt")

            os.makedirs(prod_dir, exist_ok=True)

            # --------------------------------------------------
            # Check existing production model F1
            # --------------------------------------------------

            current_f1 = -1.0

            if os.path.exists(meta_path):

                with open(meta_path, "r") as f:
                    for line in f:
                        if line.startswith("F1 Score"):
                            try:
                                current_f1 = float(line.split(":")[1].strip())
                            except Exception:
                                current_f1 = -1.0

                logger.info(f"Existing Production Model F1 : {current_f1:.4f}")

            else:
                logger.info("No existing production model found — pushing directly")

            # --------------------------------------------------
            # Decision
            # --------------------------------------------------

            improvement = new_model_f1 - current_f1

            if improvement > self.MIN_IMPROVEMENT_THRESHOLD:

                logger.info(
                    f"New model is better by {improvement:.4f} — pushing to production"
                )

                # Backup old model if it exists
                if os.path.exists(prod_path):

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    backup_path = os.path.join(
                        prod_dir,
                        f"model_backup_{timestamp}.pkl"
                    )

                    shutil.copy(prod_path, backup_path)

                    logger.info(f"Old model backed up : {backup_path}")

                # Copy new model to production
                shutil.copy(source_path, prod_path)

                logger.info(f"New model pushed to production : {prod_path}")

                # Save metadata
                with open(meta_path, "w") as f:
                    f.write(f"Model Name    : {new_model_name}\n")
                    f.write(f"F1 Score      : {new_model_f1:.4f}\n")
                    f.write(f"Pushed At     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                logger.info("Model metadata saved")

                pushed = True

            else:

                logger.info(
                    f"New model (F1={new_model_f1:.4f}) is NOT better than "
                    f"current production (F1={current_f1:.4f}). Skipping push."
                )

                pushed = False

            logger.info("Model Pusher Completed")

            return {
                "pushed":        pushed,
                "new_f1":        new_model_f1,
                "previous_f1":   current_f1,
                "improvement":   improvement,
                "prod_path":     prod_path if pushed else None
            }

        except Exception as e:

            logger.error(ElectionException(e, sys))

            raise ElectionException(e, sys)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    pusher = ModelPusher()

    result = pusher.initiate_model_pusher(
        new_model_f1=0.85,
        new_model_name="Random Forest"
    )

    print("=" * 60)
    print("MODEL PUSHER RESULT")
    print("=" * 60)
    print(f"Pushed        : {result['pushed']}")
    print(f"New F1        : {result['new_f1']:.4f}")
    print(f"Previous F1   : {result['previous_f1']:.4f}")
    print(f"Improvement   : {result['improvement']:.4f}")
    print(f"Production    : {result['prod_path']}")
