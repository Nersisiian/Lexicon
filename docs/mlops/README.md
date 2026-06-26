# MLOps with MLflow & BentoML

## Tracking Experiments
- MLflow Tracking Server: `http://localhost:5000` (locally) or `http://mlflow:5000` (in cluster)
- All fraud detection runs log parameters (`model`) and metrics (`probability`).

## Model Registry
- Models are stored in MLflow Model Registry.
- To promote a model to production:
  ```bash
  mlflow models register -m /path/to/model --name fraud_ensemble
  mlflow models transition --name fraud_ensemble --version 2 --stage Production
Deployment with BentoML
Wrap the model as a BentoML service:

python
import bentoml
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
model = mlflow.pyfunc.load_model("models:/fraud_ensemble/production")
bentoml.mlflow.save_model("fraud_service", model)
Serve: bentoml serve fraud_service:latest
