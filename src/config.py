"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Project Configuration
"""

import os


class Config:

    # ===============================
    # Project Root
    # ===============================
    ROOT_DIR = os.getcwd()

    # ===============================
    # Dataset Paths
    # ===============================
    DATASET_DIR = os.path.join(ROOT_DIR, "dataset")

    LOK_SABHA_DATA = os.path.join(
        DATASET_DIR,
        "ind-lok-sabha.csv"
    )

    VIDHAN_SABHA_DATA = os.path.join(
        DATASET_DIR,
        "ind-vidhan-sabha.csv"
    )

    # ===============================
    # Artifacts
    # ===============================
    ARTIFACT_DIR = os.path.join(ROOT_DIR, "artifacts")

    RAW_DATA_DIR = os.path.join(
        ARTIFACT_DIR,
        "raw"
    )

    TRANSFORMED_DATA_DIR = os.path.join(
        ARTIFACT_DIR,
        "transformed"
    )

    MODEL_DIR = os.path.join(
        ARTIFACT_DIR,
        "models"
    )

    REPORT_DIR = os.path.join(
        ARTIFACT_DIR,
        "reports"
    )

    # ===============================
    # Logs
    # ===============================
    LOG_DIR = os.path.join(
        ROOT_DIR,
        "logs"
    )


# ===================================================
# Testing
# ===================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Configuration Loaded Successfully")
    print("=" * 60)

    print("\nProject Root")
    print(Config.ROOT_DIR)

    print("\nDataset Folder")
    print(Config.DATASET_DIR)

    print("\nLok Sabha Dataset")
    print(Config.LOK_SABHA_DATA)

    print("\nVidhan Sabha Dataset")
    print(Config.VIDHAN_SABHA_DATA)

    print("\nArtifact Folder")
    print(Config.ARTIFACT_DIR)

    print("\nRaw Data Folder")
    print(Config.RAW_DATA_DIR)

    print("\nModel Folder")
    print(Config.MODEL_DIR)

    print("\nReport Folder")
    print(Config.REPORT_DIR)

    print("\nLog Folder")
    print(Config.LOG_DIR)

    print("\n" + "=" * 60)