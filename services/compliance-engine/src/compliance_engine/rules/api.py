from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

router = APIRouter(prefix="/rules", tags=["rules"])

RULES_FILE = "rules.json"

class Condition(BaseModel):
    field: str
    operator: str  # eq, neq, gt, lt, in
    value: str

class Rule(BaseModel):
    id: Optional[str] = None
    name: str
    description: str = ""
    conditions: List[Condition]
    action: str  # "approve", "reject", "manual_review"

def load_rules() -> List[dict]:
    if not os.path.exists(RULES_FILE):
        return []
    with open(RULES_FILE, "r") as f:
        return json.load(f)

def save_rules(rules: List[dict]):
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=2)

@router.get("/")
async def get_rules():
    return load_rules()

@router.post("/")
async def create_rule(rule: Rule):
    rules = load_rules()
    new_rule = rule.dict()
    new_rule["id"] = str(len(rules) + 1)
    rules.append(new_rule)
    save_rules(rules)
    return new_rule

@router.put("/{rule_id}")
async def update_rule(rule_id: str, rule: Rule):
    rules = load_rules()
    for i, r in enumerate(rules):
        if r["id"] == rule_id:
            updated = rule.dict()
            updated["id"] = rule_id
            rules[i] = updated
            save_rules(rules)
            return updated
    raise HTTPException(404, "Rule not found")

@router.delete("/{rule_id}")
async def delete_rule(rule_id: str):
    rules = load_rules()
    rules = [r for r in rules if r["id"] != rule_id]
    save_rules(rules)
    return {"status": "deleted"}
