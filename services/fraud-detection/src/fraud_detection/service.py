import mlflow
import json
import structlog
from compliance_sdk.kafka import ResilientConsumer, KafkaClient
from compliance_sdk.observability.metrics import document_processed
from opentelemetry import trace
from prometheus_client import Counter
from .ensemble import FraudEnsemble
from .config import settings
from .ab_router import ABRouter

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

MODEL_USED = Counter('fraud_model_used_total', 'Model selected for fraud detection', ['model'])

class FraudDetectionService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="fraud-detection-v1",
            topics=[f"document.compliance.evaluated.{settings.REGULATOR_ID}"],
            dlq_topic="document.fraud.dlq",
        )
        self._kafka = kafka
        # Загружаем модель из MLflow Model Registry, если URI задан. Иначе локально.
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI or "http://localhost:5000")
        try:
            model_uri = f"models:/{settings.MLFLOW_MODEL_NAME}/production"
            self._model = mlflow.pyfunc.load_model(model_uri)
        except:
            self._model = FraudEnsemble(settings.MODEL_PATH)
        self._router = ABRouter()

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        data = json.loads(msg.value)
        mlflow.set_experiment('fraud-assessment')
        with mlflow.start_run():
            result, model_name = self._router.predict(data)
            mlflow.log_metric('probability', result['probability'])
            mlflow.log_param('model', model_name)
        logger.info("fraud_assessment", doc_id=doc_id, prob=result["probability"], model=model_name)
        MODEL_USED.labels(model=model_name).inc()
        document_processed.labels(
            service="fraud-detection", document_type="unknown", status="fraud_checked"
        ).inc()
        await self._kafka.publish(
            "document.fraud.checked",
            key=doc_id,
            value=json.dumps(result).encode(),
        )