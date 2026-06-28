import json
import structlog
import shap
import mlflow
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
SHAP_VALUES_GENERATED = Counter('shap_values_generated_total', 'Number of SHAP explanations generated')

class FraudDetectionService:
    def __init__(self, kafka: KafkaClient):
        self.consumer = ResilientConsumer(
            bootstrap_servers=kafka.bootstrap_servers,
            group_id="fraud-detection-v1",
            topics=[f"document.compliance.evaluated.{settings.REGULATOR_ID}"],
            dlq_topic="document.fraud.dlq",
        )
        self._kafka = kafka
        self._router = ABRouter()

    async def process(self, msg) -> None:
        doc_id = msg.key.decode()
        data = json.loads(msg.value)
        result, model_name = self._router.predict(data)

        # SHAP?объ€снение
        shap_values = None
        try:
            # »спользуем модель, котора€ делала предсказание
            model = self._router.model_b if model_name == "model_b" else self._router.model_a
            if hasattr(model, 'predict_proba'):
                explainer = shap.Explainer(model.predict_proba, masker=shap.maskers.Independent(data, max_samples=100))
                shap_values = explainer(data).values.tolist()
                SHAP_VALUES_GENERATED.inc()
                logger.info("shap_explanation_generated", doc_id=doc_id, model=model_name)
        except Exception as e:
            logger.warning("shap_failed", doc_id=doc_id, error=str(e))

        # Ћогирование MLflow
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI or "http://localhost:5000")
        mlflow.set_experiment("fraud-assessment")
        with mlflow.start_run():
            mlflow.log_metric("probability", result.get("probability", 0.0))
            mlflow.log_param("model", model_name)
            if shap_values is not None:
                mlflow.log_dict({"shap_values": shap_values}, "shap.json")

        MODEL_USED.labels(model=model_name).inc()
        document_processed.labels(
            service="fraud-detection", document_type="unknown", status="fraud_checked"
        ).inc()

        # ќтправл€ем результат дальше
        await self._kafka.publish(
            "document.fraud.checked",
            key=doc_id,
            value=json.dumps(result).encode(),
        )
