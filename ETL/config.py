from enum import Enum

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Topics(Enum):
    analytics = 'analytics'


class KafkaConfig(BaseSettings):
    CONSUMER_GROUP_ID: str = 'analytics'

    SERVER0: str
    SERVER1: str
    SERVER2: str

    @computed_field
    def BOOTSTRAP_SERVERS(self) -> list[str]:
        return [self.SERVER0, self.SERVER1, self.SERVER2]

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='KAFKA_',
        extra='ignore',
    )


class ClickhouseConfig(BaseSettings):
    ANALYTICS_TABLE: str = 'movies.test_analytics'
    HOST: str = 'clickhouse'
    PORT: int = 8123

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='CLICKHOUSE_',
        extra='ignore',
    )


kafka_config = KafkaConfig()
ch_config = ClickhouseConfig()
