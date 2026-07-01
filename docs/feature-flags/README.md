# Feature Flags

## Overview
Dynamic feature toggles for A/B testing and gradual rollouts.

## Usage
```python
from compliance_sdk.feature_flags import is_enabled

if await is_enabled("new_dashboard"):
    # show new dashboard
Endpoints
GET /flags – list all flags

GET /flags/{name} – check a flag

POST /flags/{name} – set a flag
