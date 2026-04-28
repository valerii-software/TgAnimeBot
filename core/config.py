from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_name: str = ""
    admin_id: int
    bot_token: str

    pg_user: str
    pg_password: str
    pg_database: str
    pg_host: str = "localhost"
    pg_port: int = 5432

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}"
            f"@{self.pg_host}:{self.pg_port}/{self.pg_database}"
        )


settings = Settings()
