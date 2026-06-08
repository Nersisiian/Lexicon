#!/bin/bash
set -e

echo "==> Waiting for services to be healthy..."
# Ждём, пока intake-gateway не ответит 200
for i in {1..30}; do
  if curl -s -f http://localhost:8000/health > /dev/null; then
    echo "Intake Gateway is healthy"
    break
  fi
  sleep 2
done

echo "==> Uploading test document"
RESP=$(curl -s -X POST http://localhost:8000/v2/documents \
  -F "file=@scripts/sample.pdf;type=application/pdf")
DOC_ID=$(echo "$RESP" | jq -r '.document_id')
echo "Document ID: $DOC_ID"

# Ждём, пока документ пройдёт конвейер (максимум 30 секунд)
sleep 15

# Проверяем, что событие document.ingested есть в Kafka
echo "==> Verifying Kafka message"
docker-compose -f deploy/docker-compose/docker-compose.staging.yml exec kafka \
  kafka-console-consumer --topic document.ingested --bootstrap-server localhost:9092 \
  --timeout-ms 10000 | grep "$DOC_ID"

echo "==> Smoke test passed!"