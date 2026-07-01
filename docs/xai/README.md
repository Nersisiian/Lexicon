# Explainable AI (XAI) with SHAP

## Overview
The fraud detection service uses SHAP (SHapley Additive exPlanations) to provide transparency into model decisions.

## How it works
- After fraud assessment, SHAP values are computed for each feature.
- The `/v2/documents/{id}/explain` endpoint returns the explanation.
- SHAP values are logged to MLflow for further analysis.

## Usage
```bash
curl http://localhost:8000/v2/documents/abc123/explain
Future improvements
Visualize SHAP waterfall plots in the frontend.

Include explanations in audit logs.
