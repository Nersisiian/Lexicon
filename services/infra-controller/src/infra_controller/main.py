from fastapi import FastAPI
from kubernetes import client, config
import yaml

app = FastAPI(title="Infrastructure Controller", version="1.0")

@app.on_event("startup")
async def startup():
    try:
        config.load_incluster_config()
    except:
        config.load_kube_config()

@app.post("/infra/rds")
async def create_rds(instance_name: str, db_name: str, username: str, password: str):
    # Применение Crossplane-ресурса для создания RDS
    rds_yaml = {
        "apiVersion": "aws.upbound.io/v1beta1",
        "kind": "RDSInstance",
        "metadata": {"name": instance_name},
        "spec": {
            "forProvider": {
                "allocatedStorage": 20,
                "dbName": db_name,
                "engine": "postgres",
                "engineVersion": "16.1",
                "instanceClass": "db.t3.micro",
                "masterUsername": username,
                "masterUserPasswordSecretRef": {
                    "key": "password",
                    "name": f"{instance_name}-secret",
                    "namespace": "default"
                }
            }
        }
    }
    # В реальном проекте здесь будет применение через Kubernetes API
    return {"status": "applied", "resource": rds_yaml}

@app.get("/health")
async def health():
    return {"status": "ok"}
