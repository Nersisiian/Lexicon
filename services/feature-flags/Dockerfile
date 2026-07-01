FROM python:3.12-slim
WORKDIR /app
COPY services/feature-flags /app/services/feature-flags
WORKDIR /app/services/feature-flags
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8013
CMD ["uvicorn", "feature_flags.main:app", "--host", "0.0.0.0", "--port", "8013"]
