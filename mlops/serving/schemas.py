"""
Pydantic schemas for model inference API.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class SensorReading(BaseModel):
    air_temperature_k: float = Field(..., ge=250.0, le=350.0, description="Ambient air temperature in Kelvin", example=300.5)
    process_temperature_k: float = Field(..., ge=250.0, le=360.0, description="Process temperature in Kelvin", example=310.2)
    rotational_speed_rpm: float = Field(..., ge=500.0, le=4000.0, description="Spindle speed in RPM", example=1520.0)
    torque_nm: float = Field(..., ge=0.0, le=150.0, description="Applied torque in Nm", example=42.5)
    tool_wear_min: float = Field(..., ge=0.0, le=500.0, description="Tool usage time in minutes", example=120.0)

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0 = Normal Operation, 1 = Predicted Failure")
    probability: float = Field(..., description="Failure probability score")
    status: str = Field(..., description="'NORMAL' or 'WARNING: FAILURE IMMINENT'")
    model_version: str

class BatchSensorReading(BaseModel):
    readings: List[SensorReading]

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_processed: int
