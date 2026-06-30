FROM python:3.12-slim
WORKDIR /app
COPY services/sandbox-executor /app/services/sandbox-executor
WORKDIR /app/services/sandbox-executor
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8011
CMD ["uvicorn", "sandbox_executor.main:app", "--host", "0.0.0.0", "--port", "8011"]
