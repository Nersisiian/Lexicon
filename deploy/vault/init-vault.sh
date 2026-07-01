#!/bin/bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

vault secrets enable -path=lexicon kv-v2

vault kv put lexicon/database username=admin password=secret123
vault kv put lexicon/slack webhook_url=https://hooks.slack.com/services/...
vault kv put lexicon/smtp host=smtp.example.com port=587 user=noreply@example.com password=mailpass
