import pytest
import requests
import numpy as np
from src.models.sample_model import create_sample_data

BASE_URL = "http://localhost:8080"

@pytest.fixture
def sample_data():
    X, y = create_sample_data()
    return X[:5], y[:5]  # Use first 5 samples for testing

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_model_deployment():
    """Test model deployment endpoint"""
    response = requests.post(
        f"{BASE_URL}/v1/models/random_forest_model/deploy",
        json={"model_version": "1"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_model_prediction(sample_data):
    """Test model prediction endpoint"""
    # First deploy the model
    test_model_deployment()

    X, _ = sample_data
    
    # Convert features to list format for JSON serialization
    features = X.tolist()
    
    # Make prediction request
    response = requests.post(
        f"{BASE_URL}/v1/models/random_forest_model/predictions",
        json=features
    )
    
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) == len(features)
    assert all(isinstance(pred, (int, float)) for pred in predictions)

def test_experiment_creation():
    """Test experiment creation endpoint"""
    experiment_config = {
        "model_variants": {
            "variant_a": "1",
            "variant_b": "2"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/experiments/test_experiment/start",
        json=experiment_config
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"