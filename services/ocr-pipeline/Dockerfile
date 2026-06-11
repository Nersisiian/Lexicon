FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0
COPY packages/compliance-sdk /app/packages/compliance-sdk
COPY services/ocr-pipeline /app/services/ocr-pipeline
WORKDIR /app/services/ocr-pipeline
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
WORKDIR /app/services/ocr-pipeline
EXPOSE 8000
CMD ["python", "-m", "src.ocr_pipeline.main"]



# force rebuild 20260611112308
