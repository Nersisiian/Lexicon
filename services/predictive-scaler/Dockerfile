FROM python:3.12-slim
WORKDIR /app
COPY services/predictive-scaler /app/services/predictive-scaler
WORKDIR /app/services/predictive-scaler
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8019
CMD ["uvicorn", "predictive_scaler.main:app", "--host", "0.0.0.0", "--port", "8019"]
