"""
Author : Kavya Parnami
Project : Election Analytics Platform
Description : Model Training
"""

import os
import sys
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from src.logger import logger
from src.exception import ElectionException
from src.config import Config


class ModelTrainer:

    def initiate_model_training(self):

        try:

            logger.info("Model Training Started")

            path = os.path.join(
                Config.TRANSFORMED_DATA_DIR,
                "lok_sabha_clean.csv"
            )

            df = pd.read_csv(path)

            X = df[
                [
                    "year",
                    "st_name",
                    "pc_type",
                    "cand_sex",
                    "electors"
                ]
            ]

            y = df["totvotpoll"]

            categorical = [
                "st_name",
                "pc_type",
                "cand_sex"
            ]

            numerical = [
                "year",
                "electors"
            ]

            preprocessor = ColumnTransformer(

                transformers=[

                    (
                        "cat",
                        Pipeline(
                            [
                                (
                                    "imputer",
                                    SimpleImputer(strategy="most_frequent")
                                ),
                                (
                                    "encoder",
                                    OneHotEncoder(handle_unknown="ignore")
                                )
                            ]
                        ),
                        categorical
                    ),

                    (
                        "num",
                        Pipeline(
                            [
                                (
                                    "imputer",
                                    SimpleImputer(strategy="median")
                                )
                            ]
                        ),
                        numerical
                    )

                ]

            )

            X_train, X_test, y_train, y_test = train_test_split(

                X,
                y,
                test_size=0.2,
                random_state=42

            )

            models = {

                "Linear Regression": LinearRegression(),

                "Decision Tree": DecisionTreeRegressor(random_state=42),

                "Random Forest": RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                )

            }

            best_score = -1

            best_model = None

            for name, model in models.items():

                pipeline = Pipeline(

                    [

                        ("preprocessor", preprocessor),

                        ("model", model)

                    ]

                )

                pipeline.fit(X_train, y_train)

                prediction = pipeline.predict(X_test)

                score = r2_score(y_test, prediction)

                print(f"{name} : {score:.4f}")

                logger.info(f"{name} : {score}")

                if score > best_score:

                    best_score = score

                    best_model = pipeline

            os.makedirs(Config.MODEL_DIR, exist_ok=True)

            joblib.dump(

                best_model,

                os.path.join(
                    Config.MODEL_DIR,
                    "best_model.pkl"
                )

            )

            print("\nBest Score :", best_score)

            logger.info("Best Model Saved")

            return best_model

        except Exception as e:

            raise ElectionException(e, sys)


if __name__ == "__main__":

    trainer = ModelTrainer()

    trainer.initiate_model_training()