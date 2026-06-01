"""Test harness that spins up infrastructure containers."""
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
async def kafka():
    with KafkaContainer() as k:
        yield f"{k.get_container_host_ip()}:{k.get_exposed_port(9093)}"

@pytest.fixture(scope="session")
async def postgres():
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url()

@pytest.fixture(scope="session")
async def redis():
    with RedisContainer() as r:
        yield f"redis://{r.get_container_host_ip()}:{r.get_exposed_port(6379)}"
