"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Model Evaluation Component
"""

import os
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


class ModelEvaluation:
    """
    Evaluates the saved best_model.pkl (RandomForestClassifier)
    on a held-out split of the Lok Sabha engineered dataset.

    The model was trained on manually one-hot-encoded data, so
    this class uses PredictionHelper to handle encoding.
    """

    def initiate_model_evaluation(self, best_model=None, best_model_name="best_model"):

        try:

            logger.info("=" * 50)
            logger.info("Model Evaluation Started")
            logger.info("=" * 50)

            # --------------------------------------------------
            # Load model
            # --------------------------------------------------

            if best_model is None:
                model_path = os.path.join(Config.MODEL_DIR, "best_model.pkl")
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model not found : {model_path}")
                best_model = Utils.load_object(model_path)
                logger.info(f"Model loaded : {model_path}")

            # --------------------------------------------------
            # Load Lok Sabha engineered data
            # --------------------------------------------------

            data_path = os.path.join(
                Config.TRANSFORMED_DATA_DIR,
                "lok_sabha_engineered.csv"
            )

            if not os.path.exists(data_path):
                data_path = os.path.join(
                    Config.TRANSFORMED_DATA_DIR,
                    "lok_sabha_clean.csv"
                )

            df = Utils.read_csv(data_path)

            logger.info(f"Evaluation dataset shape : {df.shape}")

            # --------------------------------------------------
            # Recreate winner column if missing
            # --------------------------------------------------

            if "winner" not in df.columns:
                df["winner"] = (
                    df.groupby(["year", "pc_no"])["totvotpoll"]
                      .transform("max")
                      .eq(df["totvotpoll"])
                      .astype(int)
                )

            y = df["winner"]

            # --------------------------------------------------
            # Encode features using PredictionHelper
            # --------------------------------------------------

            from src.components.prediction import PredictionHelper

            helper = PredictionHelper()

            records = df[["year", "st_name", "pc_no", "pc_type", "cand_sex", "electors"]].to_dict(
                orient="records"
            )

            X = pd.concat(
                [helper._encode(r) for r in records],
                ignore_index=True
            )

            logger.info(f"Encoded features shape : {X.shape}")

            # --------------------------------------------------
            # Train / test split (same seed as training)
            # --------------------------------------------------

            _, X_test, _, y_test = train_test_split(
                X, y,
                test_size=0.20,
                random_state=42,
                stratify=y
            )

            # --------------------------------------------------
            # Predict
            # --------------------------------------------------

            y_pred = best_model.predict(X_test)

            # --------------------------------------------------
            # Metrics
            # --------------------------------------------------

            accuracy  = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall    = recall_score(y_test, y_pred, zero_division=0)
            f1        = f1_score(y_test, y_pred, zero_division=0)
            cm        = confusion_matrix(y_test, y_pred)

            report_text = classification_report(
                y_test, y_pred,
                target_names=["Not Winner", "Winner"],
                zero_division=0
            )

            logger.info(f"Model       : {best_model_name}")
            logger.info(f"Accuracy    : {accuracy:.4f}")
            logger.info(f"Precision   : {precision:.4f}")
            logger.info(f"Recall      : {recall:.4f}")
            logger.info(f"F1 Score    : {f1:.4f}")
            logger.info(f"Confusion Matrix :\n{cm}")
            logger.info(f"\nClassification Report :\n{report_text}")

            # --------------------------------------------------
            # Save report CSV
            # --------------------------------------------------

            os.makedirs(Config.REPORT_DIR, exist_ok=True)

            report_df = pd.DataFrame([{
                "Model":     best_model_name,
                "Accuracy":  round(accuracy, 4),
                "Precision": round(precision, 4),
                "Recall":    round(recall, 4),
                "F1 Score":  round(f1, 4),
            }])

            report_path = os.path.join(Config.REPORT_DIR, "evaluation_report.csv")
            Utils.save_csv(report_df, report_path)

            logger.info(f"Report saved : {report_path}")
            logger.info("Model Evaluation Completed Successfully")

            return {
                "model_name": best_model_name,
                "accuracy":   accuracy,
                "precision":  precision,
                "recall":     recall,
                "f1_score":   f1,
                "report":     report_df
            }

        except Exception as e:
            logger.error(ElectionException(e, sys))
            raise ElectionException(e, sys)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    evaluator = ModelEvaluation()
    metrics   = evaluator.initiate_model_evaluation()

    print("=" * 60)
    print("MODEL EVALUATION COMPLETE")
    print("=" * 60)
    print(f"Model     : {metrics['model_name']}")
    print(f"Accuracy  : {metrics['accuracy']:.4f}")
    print(f"Precision : {metrics['precision']:.4f}")
    print(f"Recall    : {metrics['recall']:.4f}")
    print(f"F1 Score  : {metrics['f1_score']:.4f}")
