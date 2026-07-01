FROM python:3.12-slim
WORKDIR /app
COPY services/self-healing-operator /app/services/self-healing-operator
WORKDIR /app/services/self-healing-operator
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
CMD ["kopf", "run", "-m", "self_healing_operator.main"]
