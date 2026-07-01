FROM python:3.12-slim
WORKDIR /app
COPY services/cost-monitor /app/services/cost-monitor
WORKDIR /app/services/cost-monitor
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8017
CMD ["uvicorn", "cost_monitor.main:app", "--host", "0.0.0.0", "--port", "8017"]
