import kopf
import kubernetes
from kubernetes.client import CoreV1Api, AppsV1Api
from kubernetes.client.rest import ApiException
import asyncio
import logging

logger = logging.getLogger(__name__)

HEALING_INTERVAL = 60  # проверка каждые 60 секунд

async def check_pod_health(pod_name, namespace):
    """ѕровер€ет, отвечает ли под на health?check."""
    try:
        # ѕытаемс€ получить статус пода
        api = CoreV1Api()
        pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
        if pod.status.phase == "Running":
            return True
    except ApiException:
        pass
    return False

async def heal_pod(pod_name, namespace):
    """¬осстанавливает под: удал€ет его, чтобы Deployment пересоздал."""
    api = CoreV1Api()
    try:
        api.delete_namespaced_pod(name=pod_name, namespace=namespace)
        logger.info(f"Pod {pod_name} deleted for healing")
    except ApiException as e:
        logger.error(f"Failed to heal pod {pod_name}: {e}")

@kopf.timer('apps/v1', 'deployments', interval=HEALING_INTERVAL)
async def self_healing(namespace, name, **kwargs):
    """ѕровер€ет все поды деплоймента и лечит нездоровые."""
    api = AppsV1Api()
    try:
        deployment = api.read_namespaced_deployment(name=name, namespace=namespace)
        selector = deployment.spec.selector.match_labels
        label_selector = ",".join([f"{k}={v}" for k, v in selector.items()])

        core_api = CoreV1Api()
        pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=label_selector)

        for pod in pods.items:
            if pod.status.phase != "Running":
                await heal_pod(pod.metadata.name, namespace)
            else:
                # ƒополнительно провер€ем, отвечает ли под
                healthy = await check_pod_health(pod.metadata.name, namespace)
                if not healthy:
                    await heal_pod(pod.metadata.name, namespace)
    except ApiException as e:
        logger.error(f"Error in self?healing for {name}: {e}")
