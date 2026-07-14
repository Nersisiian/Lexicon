FROM python:3.12-slim
WORKDIR /app
COPY services/federation-gateway /app/services/federation-gateway
WORKDIR /app/services/federation-gateway
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8018
CMD ["uvicorn", "federation_gateway.main:app", "--host", "0.0.0.0", "--port", "8018"]
