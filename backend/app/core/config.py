from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SDG Policy Intelligence Agent"
    app_env: str = "development"
    chroma_dir: str = "./storage/chroma"
    openai_api_key: str = ""
    allowed_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
