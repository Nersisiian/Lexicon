"""Completeness validator based on document type.
Extracted from legacy monolith; domain logic remains unchanged.
"""
from __future__ import annotations
from typing import List

class CompletenessRule:
    def __init__(self, required_fields: List[str]):
        self.required = required_fields

    def validate(self, extracted: dict) -> dict:
        missing = [f for f in self.required if f not in extracted or not extracted[f]]
        score = 1.0 - (len(missing) / len(self.required)) if self.required else 1.0
        return {"score": score, "missing_fields": missing}

# Registry mapping document type to rules. In production this would be DBРІР‚вЂdriven.
RULES_REGISTRY = {
    "annual_report": CompletenessRule(["company_name", "fiscal_year", "revenue", "profit"]),
    "aml_kyc": CompletenessRule(["entity_name", "id_number", "address"]),
}

