from pydantic_settings import BaseSettings, SettingsConfigDict


class ClickhouseConfig(BaseSettings):
    ANALYTICS_TABLE: str = 'movies.test_analytics'
    HOST: str = 'clickhouse'
    PORT: int = 8123
    USER: str
    PASSWORD: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='CLICKHOUSE_',
        extra='ignore',
    )


ch_config = ClickhouseConfig()
