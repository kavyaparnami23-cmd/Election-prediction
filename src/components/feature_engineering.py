"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Feature Engineering Component
"""

import os
import sys
from dataclasses import dataclass

import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


# ==========================================================
# Configuration
# ==========================================================

@dataclass
class FeatureEngineeringConfig:

    preprocessor_path: str = os.path.join(
        Config.MODEL_DIR,
        "preprocessor.pkl"
    )

    engineered_lok_path: str = os.path.join(
        Config.TRANSFORMED_DATA_DIR,
        "lok_sabha_engineered.csv"
    )

    engineered_vidhan_path: str = os.path.join(
        Config.TRANSFORMED_DATA_DIR,
        "vidhan_sabha_engineered.csv"
    )


# ==========================================================
# Feature Engineering
# ==========================================================

class FeatureEngineering:
    """
    Builds derived features from clean election data and
    fits a preprocessor (ColumnTransformer) for downstream
    model training.
    """

    def __init__(self):
        self.config = FeatureEngineeringConfig()

    # ----------------------------------------------------------
    # Helper : add derived features
    # ----------------------------------------------------------

    def _add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds derived columns:
          - vote_share     : candidate votes / constituency total votes (%)
          - turnout_rate   : total votes polled / total electors (%)
          - winner         : 1 if max votes in constituency, else 0
        """

        logger.info("Adding derived features")

        df = df.copy()

        # Determine groupby key (Lok Sabha uses pc_no, Vidhan uses ac_no)
        if "pc_no" in df.columns:
            group_key = ["year", "pc_no"]
        elif "ac_no" in df.columns:
            group_key = ["year", "ac_no"]
        else:
            group_key = ["year", "st_name"]

        # Vote Share (%)
        constituency_total = df.groupby(group_key)["totvotpoll"].transform("sum")
        df["vote_share"] = (
            df["totvotpoll"] / constituency_total.replace(0, np.nan) * 100
        ).fillna(0).round(4)

        # Turnout Rate (%)
        if "electors" in df.columns:
            df["turnout_rate"] = (
                constituency_total / df["electors"].replace(0, np.nan) * 100
            ).fillna(0).round(4)
        else:
            df["turnout_rate"] = 0.0

        # Winner flag
        max_votes = df.groupby(group_key)["totvotpoll"].transform("max")
        df["winner"] = (df["totvotpoll"] == max_votes).astype(int)

        logger.info("Derived features added : vote_share, turnout_rate, winner")

        return df

    # ----------------------------------------------------------
    # Helper : build and fit preprocessor
    # ----------------------------------------------------------

    def _build_preprocessor(self, df: pd.DataFrame) -> ColumnTransformer:
        """
        Builds a ColumnTransformer that:
          - OneHotEncodes categorical columns
          - Scales numerical columns with StandardScaler
        """

        cat_cols = df.select_dtypes(include="object").columns.tolist()
        num_cols = df.select_dtypes(exclude="object").columns.tolist()

        logger.info(f"Preprocessor — Categorical : {cat_cols}")
        logger.info(f"Preprocessor — Numerical   : {num_cols}")

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "cat",
                    Pipeline([
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
                    ]),
                    cat_cols
                ),
                (
                    "num",
                    Pipeline([
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler())
                    ]),
                    num_cols
                )
            ]
        )

        return preprocessor

    # ----------------------------------------------------------
    # Main entry point
    # ----------------------------------------------------------

    def initiate_feature_engineering(self):

        try:

            logger.info("=" * 50)
            logger.info("Feature Engineering Started")
            logger.info("=" * 50)

            # Create dirs
            os.makedirs(Config.TRANSFORMED_DATA_DIR, exist_ok=True)
            os.makedirs(Config.MODEL_DIR, exist_ok=True)

            # Load clean data
            lok_path    = os.path.join(Config.TRANSFORMED_DATA_DIR, "lok_sabha_clean.csv")
            vidhan_path = os.path.join(Config.TRANSFORMED_DATA_DIR, "vidhan_sabha_clean.csv")

            lok_df    = Utils.read_csv(lok_path)
            vidhan_df = Utils.read_csv(vidhan_path)

            logger.info(f"Lok Sabha Clean Shape    : {lok_df.shape}")
            logger.info(f"Vidhan Sabha Clean Shape : {vidhan_df.shape}")

            # Add derived features
            lok_df    = self._add_features(lok_df)
            vidhan_df = self._add_features(vidhan_df)

            # Save engineered datasets
            Utils.save_csv(lok_df, self.config.engineered_lok_path)
            Utils.save_csv(vidhan_df, self.config.engineered_vidhan_path)

            logger.info("Engineered datasets saved")

            # Build preprocessor on Vidhan Sabha (used for classification)
            # Drop target + identifier columns before fitting
            target_drop = [
                "winner", "totvotpoll", "vote_share",
                "cand_name", "partyname", "partyabbre", "ac_name"
            ]

            feature_df = vidhan_df.drop(
                columns=[c for c in target_drop if c in vidhan_df.columns]
            )

            preprocessor = self._build_preprocessor(feature_df)

            preprocessor.fit(feature_df)

            # Save preprocessor
            Utils.save_object(self.config.preprocessor_path, preprocessor)

            logger.info(f"Preprocessor saved : {self.config.preprocessor_path}")
            logger.info("Feature Engineering Completed Successfully")

            return lok_df, vidhan_df, preprocessor

        except Exception as e:

            logger.error(ElectionException(e, sys))

            raise ElectionException(e, sys)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    fe = FeatureEngineering()

    lok_df, vidhan_df, preprocessor = fe.initiate_feature_engineering()

    print("=" * 60)
    print("FEATURE ENGINEERING COMPLETE")
    print("=" * 60)
    print(f"Lok Sabha    : {lok_df.shape}")
    print(f"Vidhan Sabha : {vidhan_df.shape}")
    print(f"\nNew Columns  : vote_share, turnout_rate, winner")
    print(f"\nPreprocessor : saved to {FeatureEngineeringConfig().preprocessor_path}")