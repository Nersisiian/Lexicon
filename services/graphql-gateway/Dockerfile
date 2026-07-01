FROM python:3.12-slim
WORKDIR /app
COPY services/graphql-gateway /app/services/graphql-gateway
WORKDIR /app/services/graphql-gateway
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8007
CMD ["uvicorn", "graphql_gateway.main:app", "--host", "0.0.0.0", "--port", "8007"]
