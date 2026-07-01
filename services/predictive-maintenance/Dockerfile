FROM python:3.12-slim
WORKDIR /app
COPY services/predictive-maintenance /app/services/predictive-maintenance
WORKDIR /app/services/predictive-maintenance
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8005
CMD ["uvicorn", "predictive_maintenance.main:app", "--host", "0.0.0.0", "--port", "8005"]
