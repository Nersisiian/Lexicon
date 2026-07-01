FROM python:3.12-slim
WORKDIR /app
COPY services/webhook-dispatcher /app/services/webhook-dispatcher
WORKDIR /app/services/webhook-dispatcher
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8008
CMD ["uvicorn", "webhook_dispatcher.main:app", "--host", "0.0.0.0", "--port", "8008"]
