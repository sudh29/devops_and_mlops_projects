"""
Feature engineering and preprocessing pipeline.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

class SensorFeatureEngineer(BaseEstimator, TransformerMixin):
    """Derives domain-specific thermodynamic and mechanical power features."""

    def __init__(self):
        self.feature_names_out_ = None

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_df = X.copy()
        # Thermodynamic differential
        X_df["temp_diff"] = X_df["process_temperature_k"] - X_df["air_temperature_k"]
        # Mechanical power output (kW)
        X_df["power_kw"] = (2 * np.pi * X_df["rotational_speed_rpm"] * X_df["torque_nm"]) / 60000
        # Strain index
        X_df["strain_index"] = (X_df["torque_nm"] * X_df["tool_wear_min"]) / 1000

        self.feature_names_out_ = list(X_df.columns)
        return X_df

    def get_feature_names_out(self, input_features=None):
        return np.array(self.feature_names_out_)

def build_training_pipeline(n_estimators: int = 100, max_depth: int = 6, random_state: int = 42) -> Pipeline:
    """Builds an end-to-end scikit-learn Pipeline with feature engineering and classifier."""
    pipeline = Pipeline(steps=[
        ("engineer", SensorFeatureEngineer()),
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            class_weight="balanced"
        ))
    ])
    return pipeline
