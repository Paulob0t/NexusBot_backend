import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str = "puvnex_secret_key_default"

    # JWT Authentication
    JWT_SECRET_KEY: str = "puvnex_jwt_secret_key_default_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas

    # Database (PostgreSQL por defecto)
    DB_TYPE: str = "postgresql"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "nexusbot_db"
    DATABASE_URL: str = ""

    # HostingPro DB (opcional)
    DATABASE_URL_HP: str = ""

    # CORS
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:5180",
        "http://127.0.0.1:5180",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://adm.conlineweb.com",
        "https://cliente.conlineweb.com",
    ]

    # SMTP Mail Server
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_SECURE: str = "tls"
    SMTP_AUTH: bool = True
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Puvnex CRM"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        import urllib.parse
        quoted_user = urllib.parse.quote_plus(self.DB_USER)
        quoted_pass = urllib.parse.quote_plus(self.DB_PASS) if self.DB_PASS else ""
        auth_part = f"{quoted_user}:{quoted_pass}@" if quoted_pass else (f"{quoted_user}@" if quoted_user else "")

        if self.DB_TYPE == "mysql" or self.DB_PORT == 3306:
            return f"mysql+pymysql://{auth_part}{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        return f"postgresql+psycopg2://{auth_part}{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
