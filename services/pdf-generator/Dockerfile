FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2 && rm -rf /var/lib/apt/lists/*
COPY services/pdf-generator /app/services/pdf-generator
WORKDIR /app/services/pdf-generator
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8012
CMD ["uvicorn", "pdf_generator.main:app", "--host", "0.0.0.0", "--port", "8012"]
