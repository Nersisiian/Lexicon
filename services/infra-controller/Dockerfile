FROM python:3.12-slim
WORKDIR /app
COPY services/infra-controller /app/services/infra-controller
WORKDIR /app/services/infra-controller
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8009
CMD ["uvicorn", "infra_controller.main:app", "--host", "0.0.0.0", "--port", "8009"]
