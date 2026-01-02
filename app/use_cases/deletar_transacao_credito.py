"""
Caso de Uso: Deletar Transação de Crédito
"""
from app.data.repositories.transacao_credito_repository_interface import TransacaoCreditoRepositoryInterface


class DeletarTransacaoCredito:
    """Caso de uso para deletar uma transação de crédito"""
    
    def __init__(self, repository: TransacaoCreditoRepositoryInterface):
        self.repository = repository
    
    def execute(self, row_index: int) -> bool:
        """
        Deleta uma transação de crédito
        
        Args:
            row_index: Índice da linha na planilha (>= 2)
            
        Returns:
            bool: True se deletou com sucesso
        """
        if row_index < 2:
            raise ValueError("Índice da linha deve ser >= 2 (linha 1 é o cabeçalho)")
        
        return self.repository.delete(row_index)
