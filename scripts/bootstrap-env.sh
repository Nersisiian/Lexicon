#!/usr/bin/env bash
set -euo pipefail
echo "Bootstrapping environment..."
python -m venv .venv
source .venv/bin/activate
pip install poetry
cd packages/compliance-sdk && poetry install && cd -
for svc in services/*/; do
    echo "Installing $svc"
    cd $svc
    poetry install
    cd -
done
echo "Done."