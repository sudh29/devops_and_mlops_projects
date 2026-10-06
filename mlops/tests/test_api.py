"""
Integration tests for FastAPI inference endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from serving.app import app
from data.generate_dataset import generate_data
from src.pipeline import build_training_pipeline
from src.config import settings
import joblib

@pytest.fixture(scope="module", autouse=True)
def setup_test_model():
    """Ensure a trained model exists for API testing."""
    df = generate_data(n_samples=200, random_seed=42)
    feature_cols = [
        "air_temperature_k",
        "process_temperature_k",
        "rotational_speed_rpm",
        "torque_nm",
        "tool_wear_min"
    ]
    pipeline = build_training_pipeline(n_estimators=10, max_depth=3)
    pipeline.fit(df[feature_cols], df["failure"])

    settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, settings.MODEL_ARTIFACT_PATH)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_metrics_endpoint(client):
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "ml_predictions_total" in res.text

def test_predict_endpoint(client):
    payload = {
        "air_temperature_k": 300.0,
        "process_temperature_k": 310.5,
        "rotational_speed_rpm": 1500.0,
        "torque_nm": 40.0,
        "tool_wear_min": 10.0
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data
    assert data["prediction"] in (0, 1)
    assert 0.0 <= data["probability"] <= 1.0
    assert "status" in data

def test_predict_validation_error(client):
    # Invalid negative rotational speed violates schema constraint
    payload = {
        "air_temperature_k": 300.0,
        "process_temperature_k": 310.5,
        "rotational_speed_rpm": -100.0,
        "torque_nm": 40.0,
        "tool_wear_min": 10.0
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 422
