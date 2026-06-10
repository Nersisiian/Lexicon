FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk /app/packages/compliance-sdk
COPY services/audit-ledger /app/services/audit-ledger
# force rebuild 20260610191839
WORKDIR /app/services/audit-ledger
RUN pip install poetry && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
WORKDIR /app/services/audit-ledger
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.audit_ledger.main:app", "--host", "0.0.0.0", "--port", "8000"]
