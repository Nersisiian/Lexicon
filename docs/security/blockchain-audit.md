# Blockchain Audit Trail

## Overview
Lexicon supports publishing cryptographic hashes of audit events to a Distributed Ledger Technology (DLT) for immutable proof.

## Configuration
Set `BLOCKCHAIN_ENABLED=true` in environment and provide DLT endpoint credentials.

## Supported DLTs (planned)
- Hyperledger Fabric
- Ethereum (via smart contract)

## How it works
1. Every audit event is hashed using SHA?256.
2. The hash is sent to the configured DLT.
3. The transaction ID is logged and can be used for verification.

## Verification
```bash
curl http://localhost:8001/audit/verify/<hash>
(Endpoint to be implemented)
