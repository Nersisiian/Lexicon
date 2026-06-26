# Access Control Policy

## Purpose
Ensure that access to systems and data is authorized and monitored.

## Scope
All services, CI/CD pipelines, and infrastructure components of Lexicon.

## Policy
- All access to production systems must use multi?factor authentication (MFA).
- Service accounts use short?lived tokens (GitHub Secrets, Kubernetes ServiceAccounts).
- Code review is mandatory for all changes.
- Access to sensitive data (documents, audit logs) is logged and audited.

## Review
This policy is reviewed quarterly by the RegTech Platform Engineering team.
