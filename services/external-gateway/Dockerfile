FROM python:3.12-slim
WORKDIR /app
COPY services/external-gateway /app/services/external-gateway
WORKDIR /app/services/external-gateway
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8004
CMD ["uvicorn", "external_gateway.main:app", "--host", "0.0.0.0", "--port", "8004"]
