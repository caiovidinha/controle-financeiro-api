"""
Interface do repositório de configurações
"""
from abc import ABC, abstractmethod
from typing import List
from app.domain.entities import Categoria, Status, Conta, Cartao


class ConfiguracaoRepositoryInterface(ABC):
    """
    Interface que define o contrato para repositórios de configuração
    """
    
    # Categorias
    @abstractmethod
    def get_all_categorias(self) -> List[Categoria]:
        """Obtém todas as categorias"""
        pass
    
    @abstractmethod
    def create_categoria(self, nome: str) -> Categoria:
        """Cria uma nova categoria"""
        pass
    
    @abstractmethod
    def delete_categoria(self, nome: str) -> bool:
        """Deleta uma categoria"""
        pass
    
    # Status
    @abstractmethod
    def get_all_status(self, tipo: str = None) -> List[Status]:
        """
        Obtém todos os status
        
        Args:
            tipo: Filtro opcional por tipo ("RECEITA" ou "DESPESA")
        """
        pass
    
    # Contas
    @abstractmethod
    def get_all_contas(self) -> List[Conta]:
        """Obtém todas as contas"""
        pass
    
    @abstractmethod
    def create_conta(self, nome: str) -> Conta:
        """Cria uma nova conta"""
        pass
    
    @abstractmethod
    def update_conta(self, nome_antigo: str, nome_novo: str) -> Conta:
        """Atualiza o nome de uma conta existente"""
        pass
    
    @abstractmethod
    def delete_conta(self, nome: str) -> bool:
        """Deleta uma conta"""
        pass
    
    # Cartões
    @abstractmethod
    def get_all_cartoes(self) -> List[Cartao]:
        """Obtém todos os cartões"""
        pass
    
    @abstractmethod
    def create_cartao(self, nome: str) -> Cartao:
        """Cria um novo cartão"""
        pass
    
    @abstractmethod
    def update_cartao(self, nome_antigo: str, nome_novo: str) -> Cartao:
        """Atualiza o nome de um cartão existente"""
        pass
    
    @abstractmethod
    def delete_cartao(self, nome: str) -> bool:
        """Deleta um cartão"""
        pass
