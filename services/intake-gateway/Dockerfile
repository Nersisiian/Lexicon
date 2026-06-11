ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk /app/packages/compliance-sdk
COPY services/intake-gateway /app/services/intake-gateway
WORKDIR /app/services/intake-gateway
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
ENV PYTHONPATH=/app/services/intake-gateway/src
WORKDIR /app/services/intake-gateway/src
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "intake_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]

# force rebuild 20260610210623

# force rebuild 20260611111833

# force rebuild 20260611112018


# force rebuild 20260611112308

# force rebuild 20260611191711

# force rebuild 20260611193406

