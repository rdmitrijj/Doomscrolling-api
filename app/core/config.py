from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    CORS_ALLOWED_ORIGIN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() # type: ignore[call-arg]
