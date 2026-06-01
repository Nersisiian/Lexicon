FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y libgomp1
COPY packages/compliance-sdk /app/packages/compliance-sdk
COPY services/document-classifier /app/services/document-classifier
WORKDIR /app/services/document-classifier
RUN pip install poetry && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
WORKDIR /app/services/document-classifier
EXPOSE 8000
CMD ["python", "-m", "src.document_classifier.main"]




