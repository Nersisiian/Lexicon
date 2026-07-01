FROM python:3.12-slim
WORKDIR /app
COPY services/fl-coordinator /app/services/fl-coordinator
WORKDIR /app/services/fl-coordinator
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8006
CMD ["uvicorn", "fl_coordinator.main:app", "--host", "0.0.0.0", "--port", "8006"]
