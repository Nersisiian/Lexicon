ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk /app/packages/compliance-sdk
RUN echo "Cache bust: $CACHE_BUST"
COPY services/review-workbench /app/services/review-workbench
WORKDIR /app/services/review-workbench
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /appENV PYTHONPATH=/app/services/review-workbench/src
WORKDIR /app/services/review-workbench/src
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "review_workbench.main:app", "--host", "0.0.0.0", "--port", "8000"]
