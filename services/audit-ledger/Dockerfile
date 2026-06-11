ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk /app/packages/compliance-sdk
RUN echo "Cache bust: $CACHE_BUST"
COPY services/audit-ledger /app/services/audit-ledger
WORKDIR /app/services/audit-ledger
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
ENV PYTHONPATH=/app/services/audit-ledger/src
WORKDIR /app/services/audit-ledger/src
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "audit_ledger.main:app", "--host", "0.0.0.0", "--port", "8000"]
