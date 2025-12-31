"""
Interface do repositório de transações
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.domain.entities import Transacao


class TransacaoRepositoryInterface(ABC):
    """
    Interface que define o contrato para repositórios de transação
    """
    
    @abstractmethod
    def get_all(self) -> List[Transacao]:
        """Obtém todas as transações"""
        pass
    
    @abstractmethod
    def get_paginated(self, page: int, page_size: int) -> Dict[str, Any]:
        """Obtém transações paginadas"""
        pass
