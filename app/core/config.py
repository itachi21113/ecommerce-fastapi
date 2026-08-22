from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ecommerce API"
    database_url: str

    # Direct mappings for your PostgreSQL environment variables
    postgres_user: str
    postgres_password: str
    postgres_db: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # Safely ignores any other system variables
    )


settings = Settings()