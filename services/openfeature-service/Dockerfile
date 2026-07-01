FROM python:3.12-slim
WORKDIR /app
COPY services/openfeature-service /app/services/openfeature-service
WORKDIR /app/services/openfeature-service
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8015
CMD ["uvicorn", "openfeature_service.main:app", "--host", "0.0.0.0", "--port", "8015"]
