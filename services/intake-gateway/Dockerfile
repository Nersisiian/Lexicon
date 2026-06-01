FROM python:3.12-slim AS builder
WORKDIR /app

COPY packages/compliance-sdk /app/packages/compliance-sdk
COPY services/intake-gateway /app/services/intake-gateway
WORKDIR /app/services/intake-gateway
RUN pip install poetry && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
WORKDIR /app/services/intake-gateway
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.intake_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]
