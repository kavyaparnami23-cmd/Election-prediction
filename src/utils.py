"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Utility Functions
"""

import os
import sys
import joblib
import yaml
import pandas as pd

from src.logger import logger
from src.exception import ElectionException


class Utils:
    """
    Utility Class
    """

    @staticmethod
    def create_directory(path: str):
        """
        Create directory if it doesn't exist.
        """
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created : {path}")

        except Exception as e:
            raise ElectionException(e, sys)

    @staticmethod
    def read_csv(file_path: str):
        """
        Read CSV file.
        """
        try:
            logger.info(f"Reading CSV : {file_path}")

            dataframe = pd.read_csv(file_path)

            logger.info("CSV Loaded Successfully")

            return dataframe

        except Exception as e:
            raise ElectionException(e, sys)

    @staticmethod
    def save_csv(dataframe: pd.DataFrame, file_path: str):
        """
        Save dataframe as CSV.
        """
        try:
            directory = os.path.dirname(file_path)

            if directory:
                os.makedirs(directory, exist_ok=True)

            dataframe.to_csv(file_path, index=False)

            logger.info(f"CSV Saved : {file_path}")

        except Exception as e:
            raise ElectionException(e, sys)

    @staticmethod
    def save_object(file_path: str, obj):
        """
        Save model or object using Joblib.
        """
        try:
            directory = os.path.dirname(file_path)

            if directory:
                os.makedirs(directory, exist_ok=True)

            joblib.dump(obj, file_path)

            logger.info(f"Object Saved : {file_path}")

        except Exception as e:
            raise ElectionException(e, sys)

    @staticmethod
    def load_object(file_path: str):
        """
        Load saved object.
        """
        try:
            logger.info(f"Loading Object : {file_path}")

            return joblib.load(file_path)

        except Exception as e:
            raise ElectionException(e, sys)

    @staticmethod
    def read_yaml(file_path: str):
        """
        Read YAML file.
        """
        try:
            with open(file_path, "r") as file:
                return yaml.safe_load(file)

        except Exception as e:
            raise ElectionException(e, sys)


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    try:

        print("=" * 60)
        print("Testing Utils.py")
        print("=" * 60)

        # Create Test Directory
        Utils.create_directory("artifacts/test")

        # Create Sample DataFrame
        df = pd.DataFrame({
            "State": ["Rajasthan", "Delhi", "Punjab"],
            "Votes": [50000, 80000, 62000]
        })

        # Save CSV
        Utils.save_csv(df, "artifacts/test/sample.csv")

        # Read CSV
        data = Utils.read_csv("artifacts/test/sample.csv")

        print("\nCSV Data\n")
        print(data)

        # Save Object
        sample_object = {
            "Model": "Random Forest",
            "Accuracy": 91.5
        }

        Utils.save_object(
            "artifacts/test/model.pkl",
            sample_object
        )

        # Load Object
        loaded_object = Utils.load_object(
            "artifacts/test/model.pkl"
        )

        print("\nLoaded Object\n")
        print(loaded_object)

        print("\n")
        print("=" * 60)
        print("Utils Working Successfully")
        print("=" * 60)

    except Exception as e:

        logger.error(e)

        print(e)