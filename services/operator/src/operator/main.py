import kopf
import yaml
import kubernetes
from kubernetes.client import AppsV1Api, CoreV1Api

@kopf.on.create('lexicon.dev', 'v1', 'compliancepods')
def create_fn(spec, name, namespace, logger, **kwargs):
    image = spec.get('image', 'nginx:alpine')
    replicas = spec.get('replicas', 1)

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [{
                        "name": name,
                        "image": image,
                        "ports": [{"containerPort": 80}]
                    }]
                }
            }
        }
    }

    api = AppsV1Api()
    api.create_namespaced_deployment(namespace=namespace, body=deployment)
    logger.info(f"Deployment {name} created with {replicas} replicas")

@kopf.on.delete('lexicon.dev', 'v1', 'compliancepods')
def delete_fn(name, namespace, logger, **kwargs):
    api = AppsV1Api()
    api.delete_namespaced_deployment(name=name, namespace=namespace)
    logger.info(f"Deployment {name} deleted")
