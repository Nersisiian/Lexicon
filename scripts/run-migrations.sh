#!/usr/bin/env bash
for svc in services/*/; do
    if [ -d "$svc/migrations" ]; then
        echo "Running migrations for $svc"
        cd $svc
        alembic upgrade head
        cd -
    fi
done