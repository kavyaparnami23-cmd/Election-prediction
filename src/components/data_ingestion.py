"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Data Ingestion Component
"""

import os
import sys
import shutil

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


class DataIngestion:

    def __init__(self):

        self.lok_sabha_path = Config.LOK_SABHA_DATA
        self.vidhan_sabha_path = Config.VIDHAN_SABHA_DATA

        self.raw_data_path = Config.RAW_DATA_DIR

    def initiate_data_ingestion(self):

        try:

            logger.info("=" * 50)
            logger.info("Data Ingestion Started")
            logger.info("=" * 50)

            # Create artifacts/raw directory
            Utils.create_directory(self.raw_data_path)

            # Check if datasets exist
            if not os.path.exists(self.lok_sabha_path):
                raise FileNotFoundError(
                    f"Lok Sabha Dataset not found : {self.lok_sabha_path}"
                )

            if not os.path.exists(self.vidhan_sabha_path):
                raise FileNotFoundError(
                    f"Vidhan Sabha Dataset not found : {self.vidhan_sabha_path}"
                )

            logger.info("Datasets Found Successfully")

            # Copy datasets to artifacts/raw
            shutil.copy(
                self.lok_sabha_path,
                os.path.join(self.raw_data_path, "ind-lok-sabha.csv")
            )

            shutil.copy(
                self.vidhan_sabha_path,
                os.path.join(self.raw_data_path, "ind-vidhan-sabha.csv")
            )

            logger.info("Datasets Copied to Artifacts Folder")

            # Read datasets
            lok_df = Utils.read_csv(self.lok_sabha_path)
            vidhan_df = Utils.read_csv(self.vidhan_sabha_path)

            logger.info("Datasets Loaded Successfully")

            logger.info(f"Lok Sabha Shape : {lok_df.shape}")
            logger.info(f"Vidhan Sabha Shape : {vidhan_df.shape}")

            logger.info("Data Ingestion Completed Successfully")

            return lok_df, vidhan_df

        except Exception as e:

            logger.error(ElectionException(e, sys))

            raise ElectionException(e, sys)


# ===========================================================
# Testing
# ===========================================================

if __name__ == "__main__":

    try:

        ingestion = DataIngestion()

        lok_df, vidhan_df = ingestion.initiate_data_ingestion()

        print("=" * 60)
        print("DATA INGESTION SUCCESSFUL")
        print("=" * 60)

        print("\nLok Sabha Dataset")

        print(lok_df.head())

        print("\nShape :", lok_df.shape)

        print("\nColumns :")

        print(lok_df.columns.tolist())

        print("\n" + "=" * 60)

        print("\nVidhan Sabha Dataset")

        print(vidhan_df.head())

        print("\nShape :", vidhan_df.shape)

        print("\nColumns :")

        print(vidhan_df.columns.tolist())

        print("\n" + "=" * 60)

        print("Artifacts Created Successfully")

    except Exception as e:

        print(e)