"""
Unit tests for MLOps feature engineering and pipeline.
"""
import pytest
import pandas as pd
import numpy as np
from src.pipeline import SensorFeatureEngineer, build_training_pipeline
from data.generate_dataset import generate_data

def test_feature_engineering_transformation():
    engineer = SensorFeatureEngineer()
    df = pd.DataFrame({
        "air_temperature_k": [300.0, 301.0],
        "process_temperature_k": [310.0, 312.0],
        "rotational_speed_rpm": [1500.0, 1600.0],
        "torque_nm": [40.0, 50.0],
        "tool_wear_min": [50.0, 60.0]
    })

    transformed = engineer.transform(df)

    assert "temp_diff" in transformed.columns
    assert "power_kw" in transformed.columns
    assert "strain_index" in transformed.columns
    assert transformed["temp_diff"].iloc[0] == pytest.approx(10.0)

def test_pipeline_fit_predict():
    df = generate_data(n_samples=200, random_seed=123)
    feature_cols = [
        "air_temperature_k",
        "process_temperature_k",
        "rotational_speed_rpm",
        "torque_nm",
        "tool_wear_min"
    ]
    X = df[feature_cols]
    y = df["failure"]

    pipeline = build_training_pipeline(n_estimators=10, max_depth=3)
    pipeline.fit(X, y)

    preds = pipeline.predict(X)
    probas = pipeline.predict_proba(X)

    assert len(preds) == len(df)
    assert probas.shape == (len(df), 2)
    assert set(np.unique(preds)).issubset({0, 1})
