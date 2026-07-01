FROM python:3.12-slim
WORKDIR /app
COPY services/data-catalog /app/services/data-catalog
WORKDIR /app/services/data-catalog
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8016
CMD ["uvicorn", "data_catalog.main:app", "--host", "0.0.0.0", "--port", "8016"]
