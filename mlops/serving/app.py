"""
FastAPI Model Serving Microservice with Prometheus Observability.
"""
import time
from contextlib import asynccontextmanager
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from src.config import settings
from serving.schemas import (
    SensorReading,
    PredictionResponse,
    BatchSensorReading,
    BatchPredictionResponse
)

# Prometheus metrics
PREDICTION_COUNT = Counter(
    "ml_predictions_total", "Total count of ML inference predictions", ["result"]
)
INFERENCE_LATENCY = Histogram(
    "ml_inference_duration_seconds", "Histogram of ML model inference latency in seconds"
)

# Model container
model_store = {
    "model": None,
    "version": "1.0.0"
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model artifact on startup
    artifact_path = settings.MODEL_ARTIFACT_PATH
    if artifact_path.exists():
        model_store["model"] = joblib.load(artifact_path)
        print(f"[INIT] Model successfully loaded from {artifact_path}")
    else:
        print("[WARN] No model artifact found on startup. Model will train on first demand or can be trained via train.py.")
    yield
    model_store["model"] = None

app = FastAPI(
    title="Predictive Maintenance Inference API",
    description="Low-latency machine learning inference service for industrial equipment telemetry.",
    version="1.0.0",
    lifespan=lifespan
)

def _get_model():
    if model_store["model"] is None:
        if settings.MODEL_ARTIFACT_PATH.exists():
            model_store["model"] = joblib.load(settings.MODEL_ARTIFACT_PATH)
        else:
            from train import train
            print("[INFO] Auto-training model for inference demo...")
            train()
            model_store["model"] = joblib.load(settings.MODEL_ARTIFACT_PATH)
    return model_store["model"]

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "model_loaded": model_store["model"] is not None or settings.MODEL_ARTIFACT_PATH.exists(),
        "version": model_store["version"]
    }

@app.get("/metrics", tags=["Observability"])
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
def predict(reading: SensorReading):
    start_time = time.time()
    try:
        model = _get_model()
        input_data = pd.DataFrame([reading.model_dump()])

        proba = float(model.predict_proba(input_data)[0, 1])
        prediction = int(proba >= 0.5)

        status_text = "WARNING: FAILURE IMMINENT" if prediction == 1 else "NORMAL"
        PREDICTION_COUNT.labels(result="failure" if prediction == 1 else "normal").inc()
        INFERENCE_LATENCY.observe(time.time() - start_time)

        return PredictionResponse(
            prediction=prediction,
            probability=round(proba, 4),
            status=status_text,
            model_version=model_store["version"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.post("/batch-predict", response_model=BatchPredictionResponse, tags=["Inference"])
def batch_predict(batch: BatchSensorReading):
    start_time = time.time()
    try:
        model = _get_model()
        records = [r.model_dump() for r in batch.readings]
        input_data = pd.DataFrame(records)

        probas = model.predict_proba(input_data)[:, 1]
        results = []

        for p in probas:
            pred = int(p >= 0.5)
            PREDICTION_COUNT.labels(result="failure" if pred == 1 else "normal").inc()
            results.append(
                PredictionResponse(
                    prediction=pred,
                    probability=round(float(p), 4),
                    status="WARNING: FAILURE IMMINENT" if pred == 1 else "NORMAL",
                    model_version=model_store["version"]
                )
            )

        INFERENCE_LATENCY.observe(time.time() - start_time)
        return BatchPredictionResponse(
            predictions=results,
            total_processed=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch inference error: {str(e)}")
