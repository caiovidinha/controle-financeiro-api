"""
Casos de Uso para Saldos
"""
from typing import List
from app.domain.entities import Saldo, SaldoConta
from app.data.repositories.google_sheets_api_repository import GoogleSheetsAPIRepository


class ObterSaldoGeral:
    """Caso de uso para obter o saldo geral"""
    
    def __init__(self, repository: GoogleSheetsAPIRepository):
        self.repository = repository
    
    def execute(self) -> Saldo:
        """
        Obtém o saldo geral
        
        Returns:
            Entidade Saldo
        """
        return self.repository.get_saldo_geral()


class ObterSaldoPorConta:
    """Caso de uso para obter o saldo por conta"""
    
    def __init__(self, repository: GoogleSheetsAPIRepository):
        self.repository = repository
    
    def execute(self) -> List[SaldoConta]:
        """
        Obtém a lista de saldos por conta
        
        Returns:
            Lista de entidades SaldoConta
        """
        return self.repository.get_saldo_por_conta()
