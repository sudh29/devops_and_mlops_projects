"""
Training pipeline with MLflow tracking and artifact generation.
"""
import os
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

import mlflow
import mlflow.sklearn

from data.generate_dataset import generate_data
from src.config import settings
from src.pipeline import build_training_pipeline

def train():
    print("[1/5] Preparing training dataset...")
    data_file = settings.RAW_DATA_PATH
    if data_file.exists():
        df = pd.read_csv(data_file)
    else:
        df = generate_data()
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(data_file, index=False)

    feature_cols = [
        "air_temperature_k",
        "process_temperature_k",
        "rotational_speed_rpm",
        "torque_nm",
        "tool_wear_min"
    ]
    X = df[feature_cols]
    y = df["failure"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=settings.RANDOM_STATE, stratify=y
    )

    print(f"[2/5] Training data: {len(X_train)} samples, Test: {len(X_test)} samples")

    # Set up MLflow tracking
    use_mlflow = False
    try:
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)
        use_mlflow = True
    except Exception as e:
        print(f"[WARN] MLflow server unreachable at {settings.MLFLOW_TRACKING_URI}. Running with local artifact logging.")

    pipeline = build_training_pipeline(
        n_estimators=settings.N_ESTIMATORS,
        max_depth=settings.MAX_DEPTH,
        random_state=settings.RANDOM_STATE
    )

    print("[3/5] Fitting pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    print("[4/5] Evaluating performance...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba))
    }

    for k, v in metrics.items():
        print(f"  - {k}: {v:.4f}")

    # Baseline gate check
    if metrics["f1_score"] < 0.60:
        raise ValueError(f"Model failed F1 baseline threshold: {metrics['f1_score']:.4f} < 0.60")

    # Save local artifact
    print("[5/5] Saving model artifact...")
    settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, settings.MODEL_ARTIFACT_PATH)
    print(f"[PASS] Model artifact saved to: {settings.MODEL_ARTIFACT_PATH}")

    # Log to MLflow if enabled
    if use_mlflow:
        try:
            with mlflow.start_run(run_name="random_forest_maintenance_model"):
                mlflow.log_params({
                    "n_estimators": settings.N_ESTIMATORS,
                    "max_depth": settings.MAX_DEPTH,
                    "random_state": settings.RANDOM_STATE,
                })
                mlflow.log_metrics(metrics)
                mlflow.sklearn.log_model(
                    sk_model=pipeline,
                    artifact_path="model",
                    registered_model_name="PredictiveMaintenanceClassifier"
                )
                print("[PASS] MLflow run logged successfully!")
        except Exception as e:
            print(f"[WARN] Failed to write to MLflow tracking: {e}")

    return metrics

if __name__ == "__main__":
    train()
