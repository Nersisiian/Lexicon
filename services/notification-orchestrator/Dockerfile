ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk /app/packages/compliance-sdk
RUN echo "Cache bust: $CACHE_BUST"
COPY services/notification-orchestrator /app/services/notification-orchestrator
WORKDIR /app/services/notification-orchestrator
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /appWORKDIR /app/services/notification-orchestrator
EXPOSE 8000
CMD ["python", "-m", "src.notification_orchestrator.main"]
