# Blockchain Audit Trail with Block?Cypher

## Overview
Lexicon publishes cryptographic hashes of audit events to the Ethereum test network via Block?Cypher API.

## Configuration
1. Set `BLOCKCHAIN_ENABLED=true` in environment.
2. Ensure outbound access to `https://api.blockcypher.com`.

## How it works
1. Every audit event is hashed (SHA?256).
2. The hash is sent to Block?Cypher test network endpoint.
3. The returned transaction ID is logged.

## Verification
Visit `https://live.blockcypher.com/eth-test/tx/<txid>` to verify the hash on-chain.
