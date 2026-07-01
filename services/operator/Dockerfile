FROM python:3.12-slim
WORKDIR /app
COPY services/operator /app/services/operator
WORKDIR /app/services/operator
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
CMD ["kopf", "run", "-m", "operator.main"]
