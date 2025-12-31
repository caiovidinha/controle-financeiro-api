"""
Use Case: Verificar saúde da aplicação
"""
from app.data.repositories.transacao_repository_interface import TransacaoRepositoryInterface


class VerificarSaude:
    """
    Caso de uso para verificar a saúde da aplicação
    """
    
    def __init__(self, repository: TransacaoRepositoryInterface):
        """
        Inicializa o caso de uso
        
        Args:
            repository: Repositório de transações
        """
        self.repository = repository
    
    def execute(self) -> dict:
        """
        Verifica a conexão com o Google Sheets
        
        Returns:
            Dicionário com status da aplicação
        """
        try:
            # Tenta obter dados para verificar a conexão
            self.repository.get_all()
            return {
                "status": "ok",
                "google_sheets": "connected",
                "error": None
            }
        except Exception as e:
            return {
                "status": "error",
                "google_sheets": "disconnected",
                "error": str(e)
            }
