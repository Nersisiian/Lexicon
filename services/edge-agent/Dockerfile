FROM python:3.12-slim
WORKDIR /app
COPY services/edge-agent /app/services/edge-agent
WORKDIR /app/services/edge-agent
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8018
CMD ["uvicorn", "edge_agent.main:app", "--host", "0.0.0.0", "--port", "8018"]
