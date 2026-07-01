# HashiCorp Vault Integration

## Overview
Vault is used for secure storage and management of secrets (passwords, API keys, tokens).

## Local Development
```bash
docker compose -f deploy/docker-compose/docker-compose.test.yml up -d vault
bash deploy/vault/init-vault.sh
Production Integration
Use Vault Agent Injector to automatically inject secrets into pods.

Configure Kubernetes auth method for service accounts.

Store CI/CD secrets in Vault and reference them via GitHub Actions.

Access
UI: http://localhost:8200

Token: root (dev mode only)
