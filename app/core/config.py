"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação carregadas de variáveis de ambiente"""
    
    # Informações da API
    app_name: str = "API Controle Financeiro"
    app_version: str = "1.0.0"
    app_description: str = "API para gerenciar transações financeiras através do Google Sheets"
    
    # Google Sheets
    google_sheets_id: str
    google_service_account_email: str
    google_private_key: str
    google_sheet_name: str = "Extrato"
    
    # CORS
    cors_origins: list = ["*"]
    
    # Paginação
    default_page_size: int = 10
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna as configurações da aplicação (singleton)
    """
    return Settings()
