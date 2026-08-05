"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Data Validation Component
"""

import os
import sys

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


class DataValidation:

    def __init__(self):

        self.lok_path = os.path.join(
            Config.RAW_DATA_DIR,
            "ind-lok-sabha.csv"
        )

        self.vidhan_path = os.path.join(
            Config.RAW_DATA_DIR,
            "ind-vidhan-sabha.csv"
        )

    # -----------------------------------------
    # Empty Dataset Check
    # -----------------------------------------

    def check_dataset_empty(self, df):

        return df.empty

    # -----------------------------------------
    # Required Columns
    # -----------------------------------------

    def check_required_columns(self, df, required_columns):

        missing_columns = []

        for column in required_columns:

            if column not in df.columns:

                missing_columns.append(column)

        return missing_columns

    # -----------------------------------------
    # Duplicate Rows
    # -----------------------------------------

    def check_duplicates(self, df):

        return df.duplicated().sum()

    # -----------------------------------------
    # Missing Values
    # -----------------------------------------

    def check_missing_values(self, df):

        return df.isnull().sum()

    # -----------------------------------------
    # Negative Values
    # -----------------------------------------

    def check_negative_values(self, df):

        invalid_votes = 0
        invalid_electors = 0

        if "totvotpoll" in df.columns:

            invalid_votes = (df["totvotpoll"] < 0).sum()

        if "electors" in df.columns:

            invalid_electors = (df["electors"] < 0).sum()

        return invalid_votes, invalid_electors

    # -----------------------------------------
    # Complete Validation
    # -----------------------------------------

    def validate(self):

        try:

            logger.info("Starting Data Validation")

            lok_df = Utils.read_csv(self.lok_path)
            vidhan_df = Utils.read_csv(self.vidhan_path)

            datasets = {
                "Lok Sabha": lok_df,
                "Vidhan Sabha": vidhan_df
            }

            required_columns = [
                "st_name",
                "year",
                "cand_name",
                "partyname",
                "totvotpoll",
                "electors"
            ]

            validation_results = {}

            for name, df in datasets.items():

                logger.info(f"Validating {name}")

                validation_results[name] = {

                    "Dataset Empty":
                        self.check_dataset_empty(df),

                    "Missing Columns":
                        self.check_required_columns(
                            df,
                            required_columns
                        ),

                    "Duplicate Rows":
                        self.check_duplicates(df),

                    "Missing Values":
                        self.check_missing_values(df).to_dict(),

                    "Invalid Votes":
                        self.check_negative_values(df)[0],

                    "Invalid Electors":
                        self.check_negative_values(df)[1]
                }

            logger.info("Validation Completed Successfully")

            return validation_results

        except Exception as e:

            logger.error(ElectionException(e, sys))

            raise ElectionException(e, sys)


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    validator = DataValidation()

    report = validator.validate()

    print("\n" + "=" * 70)
    print("DATA VALIDATION REPORT")
    print("=" * 70)

    for dataset, result in report.items():

        print(f"\n{dataset}")
        print("-" * 70)

        for key, value in result.items():

            print(f"{key} : {value}")

    print("\n" + "=" * 70)
    print("Validation Completed Successfully")
    print("=" * 70)