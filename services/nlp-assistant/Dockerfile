FROM python:3.12-slim
WORKDIR /app
COPY services/nlp-assistant /app/services/nlp-assistant
WORKDIR /app/services/nlp-assistant
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8010
CMD ["uvicorn", "nlp_assistant.main:app", "--host", "0.0.0.0", "--port", "8010"]
