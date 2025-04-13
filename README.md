# ML Model Serving Platform

A scalable platform for deploying and serving machine learning models with support for automatic A/B testing, model versioning, and real-time performance monitoring.

## Features

- FastAPI-based model serving with high performance
- Kubernetes deployment for scalability
- MLflow integration for model versioning and tracking
- Prometheus metrics for monitoring
- Automatic A/B testing support
- Health checks and readiness probes
- Secure by default with non-root containers

## Prerequisites

- Docker
- Kubernetes cluster (local or cloud)
- Python 3.11+
- kubectl CLI
- MLflow server

## Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/ritikchawla/ml-serving-platform.git
cd ml-serving-platform
```

2. **Create a Python virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start MLflow server:**
```bash
mlflow server --host 0.0.0.0 --port 5000
```

5. **Train the sample model:**
```bash
python src/models/sample_model.py
```

6. **Build and push the Docker image:**
```bash
docker build -t ml-serving-platform:latest .
```

7. **Create Kubernetes namespace:**
```bash
kubectl create namespace ml-serving
```

8. **Deploy to Kubernetes:**
```bash
kubectl apply -f kubernetes/deployment.yaml
```

9. **Wait for the deployment to be ready:**
```bash
kubectl -n ml-serving get pods -w
```

## Testing

1. **Run unit tests:**
```bash
pytest tests/
```

2. **Test the API endpoints:**

Health check:
```bash
curl http://localhost:8080/health
```

Make predictions:
```bash
curl -X POST http://localhost:8080/v1/models/random_forest_model/predictions \
  -H "Content-Type: application/json" \
  -d '[[1.0, 2.0, 3.0, 4.0]]'
```

## Monitoring

The platform exposes Prometheus metrics at `:8000/metrics`. You can configure your Prometheus instance to scrape these metrics for:

- Request latency
- Request count
- Model performance metrics
- System metrics

## Security

The platform implements several security best practices:

- Non-root container execution
- Read-only root filesystem
- Dropped capabilities
- Resource limits
- Network policies
- Secure service configuration

## API Reference

### Model Management

- `POST /v1/models/{model_name}/deploy`
  - Deploy a model version
  - Body: `{"model_version": "string"}`

- `POST /v1/models/{model_name}/predictions`
  - Get predictions from a model
  - Body: Array of feature arrays

### Experiment Management

- `POST /v1/experiments/{experiment_name}/start`
  - Start an A/B testing experiment
  - Body: `{"model_variants": {"variant_name": "version"}}`

### Health Check

- `GET /health`
  - Check service health
  - Returns: `{"status": "healthy", "timestamp": "ISO-8601 timestamp"}`