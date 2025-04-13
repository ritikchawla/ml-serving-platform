from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, start_http_server
import mlflow
import numpy as np
import os
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel

app = FastAPI(title="ML Model Serving Platform")

# Prometheus metrics
PREDICTION_REQUEST_COUNT = Counter(
    'prediction_requests_total',
    'Total number of prediction requests'
)

PREDICTION_LATENCY = Histogram(
    'prediction_latency_seconds',
    'Time spent processing prediction requests'
)

MODEL_VERSIONS = {}
ACTIVE_EXPERIMENTS = {}

class ModelDeployment(BaseModel):
    model_version: str

class ExperimentConfig(BaseModel):
    model_variants: Dict[str, str]

@app.on_event("startup")
async def startup_event():
    # Start Prometheus metrics server
    start_http_server(8000)
    
    # Initialize MLflow
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/v1/models/{model_name}/predictions")
async def predict(model_name: str, features: List[List[float]]):
    PREDICTION_REQUEST_COUNT.inc()
    
    with PREDICTION_LATENCY.time():
        try:
            if model_name not in MODEL_VERSIONS:
                raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
            
            model = MODEL_VERSIONS[model_name]
            predictions = model.predict(np.array(features))
            
            return {
                "model_name": model_name,
                "predictions": predictions.tolist(),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/models/{model_name}/deploy")
async def deploy_model(model_name: str, config: ModelDeployment):
    try:
        model_path = f"runs:/f4f1ffcdc10f4edd8db08759f51d63a7/random_forest_model"
        model = mlflow.pyfunc.load_model(model_path)
        MODEL_VERSIONS[model_name] = model
        return {
            "status": "success",
            "message": f"Model {model_name} version {config.model_version} deployed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/experiments/{experiment_name}/start")
async def start_experiment(experiment_name: str, config: ExperimentConfig):
    try:
        ACTIVE_EXPERIMENTS[experiment_name] = {
            "variants": config.model_variants,
            "start_time": datetime.now().isoformat()
        }
        return {
            "status": "success",
            "message": f"Experiment {experiment_name} started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))