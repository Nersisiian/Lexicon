FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends bpfcc-tools && rm -rf /var/lib/apt/lists/*
COPY services/ebpf-agent /app/services/ebpf-agent
WORKDIR /app/services/ebpf-agent
RUN pip install poetry==1.8.5 && poetry config virtualenvs.create false && rm -f poetry.lock && poetry install --no-root
EXPOSE 8014
CMD ["uvicorn", "ebpf_agent.main:app", "--host", "0.0.0.0", "--port", "8014"]
