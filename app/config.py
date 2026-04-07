"""
Clarear Psicologia — Configuração via variáveis de ambiente.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação carregadas do .env."""

    APP_NAME: str = "Clarear Psicologia"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./clarear.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
