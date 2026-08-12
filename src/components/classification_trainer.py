"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Classification Model Trainer Component
"""

import os
import sys
import joblib
import pandas as pd

from src.config import Config
from src.logger import logger
from src.exception import ElectionException

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

# Classification Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)
from xgboost import XGBClassifier

# Evaluation Metrics
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ==========================================================
# Classification Trainer
# ==========================================================

class ClassificationTrainer:
    """
    Trains multiple classification models on Vidhan Sabha data
    to predict election winners.  Returns the best pipeline
    (by F1 score) along with an evaluation report DataFrame.
    """

    def initiate_classification_training(self):

        try:

            logger.info("=" * 50)
            logger.info("Classification Training Started")
            logger.info("=" * 50)

            # --------------------------------------------------
            # Load Dataset
            # --------------------------------------------------

            path = os.path.join(
                Config.TRANSFORMED_DATA_DIR,
                "vidhan_sabha_clean.csv"
            )

            df = pd.read_csv(path)

            logger.info(f"Dataset Loaded : {df.shape}")

            # --------------------------------------------------
            # Create Winner Target Column
            # --------------------------------------------------

            df["winner"] = (
                df.groupby(["year", "ac_no"])["totvotpoll"]
                  .transform("max")
                  .eq(df["totvotpoll"])
                  .astype(int)
            )

            logger.info("Winner column created")

            # --------------------------------------------------
            # Class Distribution
            # --------------------------------------------------

            dist = df["winner"].value_counts()
            logger.info(f"Class Distribution :\n{dist}")

            # --------------------------------------------------
            # Features & Target
            # --------------------------------------------------

            drop_cols = [
                "winner",
                "totvotpoll",
                "cand_name",
                "partyname",
                "partyabbre",
                "ac_name"
            ]

            drop_cols = [c for c in drop_cols if c in df.columns]

            X = df.drop(columns=drop_cols)
            y = df["winner"]

            # --------------------------------------------------
            # Train / Test Split
            # --------------------------------------------------

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42,
                stratify=y
            )

            logger.info(f"Train Shape : {X_train.shape}")
            logger.info(f"Test Shape  : {X_test.shape}")

            # --------------------------------------------------
            # Preprocessor
            # --------------------------------------------------

            cat_cols = X.select_dtypes(include="object").columns.tolist()
            num_cols = X.select_dtypes(exclude="object").columns.tolist()

            logger.info(f"Categorical Columns : {cat_cols}")
            logger.info(f"Numerical Columns   : {num_cols}")

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "cat",
                        Pipeline([
                            ("imputer", SimpleImputer(strategy="most_frequent")),
                            ("encoder", OneHotEncoder(handle_unknown="ignore"))
                        ]),
                        cat_cols
                    ),
                    (
                        "num",
                        Pipeline([
                            ("imputer", SimpleImputer(strategy="median"))
                        ]),
                        num_cols
                    )
                ]
            )

            # --------------------------------------------------
            # Models
            # --------------------------------------------------

            models = {
                "Logistic Regression": LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                    class_weight="balanced"
                ),
                "Decision Tree": DecisionTreeClassifier(
                    random_state=42,
                    class_weight="balanced"
                ),
                "Random Forest": RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    class_weight="balanced"
                ),
                "Gradient Boosting": GradientBoostingClassifier(
                    random_state=42
                ),
                "XGBoost": XGBClassifier(
                    random_state=42,
                    eval_metric="logloss",
                    scale_pos_weight=10
                )
            }

            # --------------------------------------------------
            # Train & Evaluate Each Model
            # --------------------------------------------------

            results = []
            best_model = None
            best_f1 = 0.0
            best_model_name = ""

            for name, model in models.items():

                logger.info(f"Training : {name}")

                pipeline = Pipeline([
                    ("preprocessor", preprocessor),
                    ("model", model)
                ])

                pipeline.fit(X_train, y_train)

                prediction = pipeline.predict(X_test)

                accuracy  = accuracy_score(y_test, prediction)
                precision = precision_score(y_test, prediction, zero_division=0)
                recall    = recall_score(y_test, prediction, zero_division=0)
                f1        = f1_score(y_test, prediction, zero_division=0)

                results.append([name, accuracy, precision, recall, f1])

                logger.info(
                    f"{name} | Accuracy={accuracy:.4f} | "
                    f"Precision={precision:.4f} | Recall={recall:.4f} | "
                    f"F1={f1:.4f}"
                )

                if f1 > best_f1:
                    best_f1 = f1
                    best_model = pipeline
                    best_model_name = name

            # --------------------------------------------------
            # Build Report DataFrame
            # --------------------------------------------------

            report_df = pd.DataFrame(
                results,
                columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score"]
            )

            logger.info(f"\nModel Comparison :\n{report_df.sort_values('F1 Score', ascending=False).to_string()}")

            # --------------------------------------------------
            # Save Best Model
            # --------------------------------------------------

            os.makedirs(Config.MODEL_DIR, exist_ok=True)

            best_model_path = os.path.join(Config.MODEL_DIR, "best_classifier.pkl")

            joblib.dump(best_model, best_model_path)

            logger.info(f"Best Model Saved : {best_model_path}")
            logger.info(f"Best Model       : {best_model_name}")
            logger.info(f"Best F1 Score    : {best_f1:.4f}")

            logger.info("Classification Training Completed Successfully")

            return best_model, best_model_name, best_f1, report_df

        except Exception as e:

            logger.error(ElectionException(e, sys))

            raise ElectionException(e, sys)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    trainer = ClassificationTrainer()

    best_model, best_name, best_score, report = trainer.initiate_classification_training()

    print("=" * 60)
    print("CLASSIFICATION TRAINING COMPLETE")
    print("=" * 60)
    print(f"\nBest Model   : {best_name}")
    print(f"Best F1      : {best_score:.4f}")
    print("\nModel Comparison :")
    print(report.sort_values("F1 Score", ascending=False).to_string(index=False))