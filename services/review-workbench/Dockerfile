ARG CACHE_BUST=0
FROM python:3.12-slim AS builder
WORKDIR /app
COPY packages/compliance-sdk
RUN echo "Cache bust: $CACHE_BUST" /app/packages/compliance-sdk
COPY services/review-workbench /app/services/review-workbench
# force rebuild 20260610191839
WORKDIR /app/services/review-workbench
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
WORKDIR /app/services/review-workbench
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.review_workbench.main:app", "--host", "0.0.0.0", "--port", "8000"]


# force rebuild 20260611112308

