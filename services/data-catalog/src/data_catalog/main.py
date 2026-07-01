from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Data Catalog", version="1.0")

datasets = []

class Dataset(BaseModel):
    name: str
    owner: str
    description: Optional[str] = ""
    endpoint: str  # GraphQL endpoint for this dataset

@app.get("/datasets")
async def list_datasets():
    return datasets

@app.post("/datasets")
async def register_dataset(dataset: Dataset):
    datasets.append(dataset)
    return dataset

@app.get("/health")
async def health():
    return {"status": "ok"}
