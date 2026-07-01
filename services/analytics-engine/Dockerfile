FROM python:3.12-slim
WORKDIR /app
COPY services/analytics-engine /app/services/analytics-engine
WORKDIR /app/services/analytics-engine
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8003
CMD ["uvicorn", "analytics_engine.main:app", "--host", "0.0.0.0", "--port", "8003"]
