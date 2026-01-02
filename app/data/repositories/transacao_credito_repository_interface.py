"""
Interface do repositório de transações de crédito
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.domain.entities import TransacaoCredito


class TransacaoCreditoRepositoryInterface(ABC):
    """
    Interface que define o contrato para repositórios de transação de crédito
    """
    
    @abstractmethod
    def get_all(
        self,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        mes: Optional[str] = None,
        situacao: Optional[str] = None,
        cartao: Optional[str] = None,
        order_by: str = "data"
    ) -> List[TransacaoCredito]:
        """Obtém todas as transações de crédito com filtros opcionais"""
        pass
    
    @abstractmethod
    def get_paginated(
        self, 
        page: int, 
        page_size: int,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        mes: Optional[str] = None,
        situacao: Optional[str] = None,
        cartao: Optional[str] = None,
        order_by: str = "data"
    ) -> Dict[str, Any]:
        """Obtém transações de crédito de forma paginada com filtros opcionais"""
        pass
    
    @abstractmethod
    def create(self, transacao: TransacaoCredito) -> TransacaoCredito:
        """Cria uma nova transação de crédito"""
        pass
    
    @abstractmethod
    def update(self, row_index: int, transacao: TransacaoCredito) -> TransacaoCredito:
        """Atualiza uma transação de crédito existente pelo índice da linha"""
        pass
    
    @abstractmethod
    def delete(self, row_index: int) -> bool:
        """Deleta uma transação de crédito pelo índice da linha"""
        pass
