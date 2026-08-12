import os
import sys
import pandas as pd

from src.logger import logger
from src.exception import ElectionException
from src.utils import Utils
from src.config import Config


class DataTransformation:

    def clean_dataset(self, df):

        logger.info("Cleaning Dataset")

        # Remove duplicates
        df = df.drop_duplicates()

        # Fill categorical missing values
        for col in ["pc_type", "ac_type", "cand_sex"]:
            if col in df.columns:
                df[col] = df[col].fillna("Unknown")

        # Fill numerical missing values
        for col in ["year", "totvotpoll", "electors"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

                if col == "totvotpoll":
                    df[col] = df[col].fillna(0)
                else:
                    df[col] = df[col].fillna(df[col].median())

                df[col] = df[col].astype(int)

        return df

    def initiate_data_transformation(self):

        try:

            os.makedirs(Config.TRANSFORMED_DATA_DIR, exist_ok=True)

            lok_df = Utils.read_csv(Config.LOK_SABHA_DATA)
            vidhan_df = Utils.read_csv(Config.VIDHAN_SABHA_DATA)

            lok_df = self.clean_dataset(lok_df)
            vidhan_df = self.clean_dataset(vidhan_df)

            Utils.save_csv(
                lok_df,
                os.path.join(
                    Config.TRANSFORMED_DATA_DIR,
                    "lok_sabha_clean.csv"
                )
            )

            Utils.save_csv(
                vidhan_df,
                os.path.join(
                    Config.TRANSFORMED_DATA_DIR,
                    "vidhan_sabha_clean.csv"
                )
            )

            logger.info("Data Transformation Completed")

            return lok_df, vidhan_df

        except Exception as e:
            raise ElectionException(e, sys)


if __name__ == "__main__":

    transformer = DataTransformation()

    lok_df, vidhan_df = transformer.initiate_data_transformation()

    print("=" * 60)
    print("DATA TRANSFORMATION SUCCESSFUL")
    print("=" * 60)

    print("Lok Sabha :", lok_df.shape)
    print("Vidhan Sabha :", vidhan_df.shape)