"""
Caso de Uso: Deletar Transação
"""
from app.data.repositories.transacao_repository_interface import TransacaoRepositoryInterface


class DeletarTransacao:
    """Caso de uso para deletar uma transação"""
    
    def __init__(self, repository: TransacaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, row_index: int) -> bool:
        """
        Deleta uma transação
        
        Args:
            row_index: Índice da linha na planilha (>= 2)
            
        Returns:
            bool: True se deletou com sucesso
        """
        if row_index < 2:
            raise ValueError("Índice da linha deve ser >= 2 (linha 1 é o cabeçalho)")
        
        return self.repository.delete(row_index)
