ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk /app/packages/compliance-sdk
RUN echo "Cache bust: $CACHE_BUST"
COPY services/reasoning-service /app/services/reasoning-service
WORKDIR /app/services/reasoning-service
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
ENV PYTHONPATH=/app/services/reasoning-service/src
WORKDIR /app/services/reasoning-service/src
EXPOSE 8000
CMD ["python", "-m", "src.reasoning_service.main"]

# force rebuild 20260612003649