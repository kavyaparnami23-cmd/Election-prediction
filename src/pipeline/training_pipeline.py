"""
Author : Kavya Parnami
Project : ElectionPulse AI
Description : Training Pipeline — orchestrates all training stages
"""

import sys
import time

from src.logger import logger
from src.exception import ElectionException

from src.components.data_ingestion      import DataIngestion
from src.components.data_validation     import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.feature_engineering import FeatureEngineering
from src.components.classification_trainer import ClassificationTrainer
from src.components.model_evaluation    import ModelEvaluation
from src.components.model_pusher        import ModelPusher


class TrainingPipeline:
    """
    Runs the complete ElectionPulse AI training pipeline:

    DataIngestion
        → DataValidation
        → DataTransformation
        → FeatureEngineering
        → ClassificationTrainer
        → ModelEvaluation
        → ModelPusher
    """

    def run(self):

        pipeline_start = time.time()

        try:

            logger.info("=" * 60)
            logger.info("TRAINING PIPELINE STARTED")
            logger.info("=" * 60)

            # ==================================================
            # Stage 1 : Data Ingestion
            # ==================================================

            logger.info("\n[ Stage 1 ] Data Ingestion")

            t0 = time.time()

            ingestion = DataIngestion()

            lok_df, vidhan_df = ingestion.initiate_data_ingestion()

            logger.info(f"Data Ingestion completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Stage 2 : Data Validation
            # ==================================================

            logger.info("\n[ Stage 2 ] Data Validation")

            t0 = time.time()

            validator = DataValidation()

            validation_results = validator.validate()

            for dataset, result in validation_results.items():
                logger.info(f"\nValidation — {dataset}")
                for key, val in result.items():
                    logger.info(f"  {key} : {val}")

            logger.info(f"Data Validation completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Stage 3 : Data Transformation
            # ==================================================

            logger.info("\n[ Stage 3 ] Data Transformation")

            t0 = time.time()

            transformer = DataTransformation()

            lok_clean, vidhan_clean = transformer.initiate_data_transformation()

            logger.info(f"Lok Sabha Clean    : {lok_clean.shape}")
            logger.info(f"Vidhan Sabha Clean : {vidhan_clean.shape}")
            logger.info(f"Data Transformation completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Stage 4 : Feature Engineering
            # ==================================================

            logger.info("\n[ Stage 4 ] Feature Engineering")

            t0 = time.time()

            fe = FeatureEngineering()

            lok_eng, vidhan_eng, preprocessor = fe.initiate_feature_engineering()

            logger.info(f"Lok Sabha Engineered    : {lok_eng.shape}")
            logger.info(f"Vidhan Sabha Engineered : {vidhan_eng.shape}")
            logger.info(f"Feature Engineering completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Stage 5 : Classification Training
            # ==================================================

            logger.info("\n[ Stage 5 ] Classification Training")

            t0 = time.time()

            trainer = ClassificationTrainer()

            best_model, best_name, best_f1, report_df = \
                trainer.initiate_classification_training()

            logger.info(f"Best Model : {best_name} | F1 = {best_f1:.4f}")
            logger.info(f"Classification Training completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Stage 6 : Model Evaluation
            # ==================================================

            logger.info("\n[ Stage 6 ] Model Evaluation")

            t0 = time.time()

            evaluator = ModelEvaluation()

            metrics = evaluator.initiate_model_evaluation(
                best_model=best_model,
                best_model_name=best_name
            )

            logger.info(
                f"Evaluation | Accuracy={metrics['accuracy']:.4f} | "
                f"F1={metrics['f1_score']:.4f}"
            )
            logger.info(f"Model Evaluation completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Stage 7 : Model Pusher
            # ==================================================

            logger.info("\n[ Stage 7 ] Model Pusher")

            t0 = time.time()

            pusher = ModelPusher()

            push_result = pusher.initiate_model_pusher(
                new_model_f1=metrics["f1_score"],
                new_model_name=best_name
            )

            if push_result["pushed"]:
                logger.info(f"Model pushed to production : {push_result['prod_path']}")
            else:
                logger.info("Model NOT pushed — existing production model is better")

            logger.info(f"Model Pusher completed in {time.time() - t0:.1f}s")

            # ==================================================
            # Done
            # ==================================================

            total_time = time.time() - pipeline_start

            logger.info("=" * 60)
            logger.info(f"TRAINING PIPELINE COMPLETED in {total_time:.1f}s")
            logger.info("=" * 60)

            return {
                "best_model_name": best_name,
                "best_f1":         best_f1,
                "metrics":         metrics,
                "push_result":     push_result
            }

        except Exception as e:

            logger.error(ElectionException(e, sys))

            raise ElectionException(e, sys)


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    pipeline = TrainingPipeline()

    result = pipeline.run()

    print("\n" + "=" * 60)
    print("TRAINING PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Best Model   : {result['best_model_name']}")
    print(f"Best F1      : {result['best_f1']:.4f}")
    print(f"Accuracy     : {result['metrics']['accuracy']:.4f}")
    print(f"Precision    : {result['metrics']['precision']:.4f}")
    print(f"Recall       : {result['metrics']['recall']:.4f}")
    print(f"F1 Score     : {result['metrics']['f1_score']:.4f}")
    print(f"Model Pushed : {result['push_result']['pushed']}")
    print("=" * 60)
