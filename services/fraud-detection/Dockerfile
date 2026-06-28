ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY services/fraud-detection/models/ /models/
COPY packages/compliance-sdk /app/packages/compliance-sdk
RUN echo "Cache bust: $CACHE_BUST"
COPY services/fraud-detection /app/services/fraud-detection
WORKDIR /app/services/fraud-detection
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
ENV PYTHONPATH=/app/services/fraud-detection/src
WORKDIR /app/services/fraud-detection/src
EXPOSE 8000
CMD ["python", "-m", "src.fraud_detection.main"]

# force rebuild 20260612003649