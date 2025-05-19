from enum import Enum

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Topics(Enum):
    analytics = 'analytics'


class KafkaConfig(BaseSettings):
    CONSUMER_GROUP_ID: str = 'analytics'
    BOOTSTRAP_SERVERS: list[str]

    SERVER0: str
    SERVER1: str
    SERVER2: str

    @field_validator("BOOTSTRAP_SERVERS", mode="before")
    def assemble_bootstrap_servers(cls, v, values):
        if v is not None:
            return v  # Если BOOTSTRAP_SERVERS передано явно

        servers = []
        for i in range(3):
            server_key = f"SERVER{i}"
            if server_key in values:
                servers.append(values[server_key])

        return servers if servers else None

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='KAFKA_',
        extra='ignore',
    )


kafka_config = KafkaConfig()
