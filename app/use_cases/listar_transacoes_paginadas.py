"""
Use Case: Listar transações de forma paginada
"""
from typing import Dict, Any
from app.data.repositories.transacao_repository_interface import TransacaoRepositoryInterface
from app.domain.entities import Transacao


class ListarTransacoesPaginadas:
    """
    Caso de uso para listar transações com paginação
    """
    
    def __init__(self, repository: TransacaoRepositoryInterface):
        """
        Inicializa o caso de uso com um repositório
        
        Args:
            repository: Repositório de transações
        """
        self.repository = repository
    
    def execute(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Executa o caso de uso
        
        Args:
            page: Número da página
            page_size: Tamanho da página
            
        Returns:
            Dicionário com dados paginados
        """
        # Validações de negócio
        if page < 1:
            raise ValueError("Página deve ser maior que 0")
        
        if page_size < 1:
            raise ValueError("Tamanho da página deve ser maior que 0")
        
        if page_size > 100:
            raise ValueError("Tamanho da página não pode exceder 100")
        
        # Delega ao repositório
        return self.repository.get_paginated(page=page, page_size=page_size)
