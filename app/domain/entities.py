"""
Entidades de domínio - Representam os conceitos de negócio
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Transacao:
    """
    Entidade que representa uma transação financeira
    """
    tipo: str
    descritivo: str
    valor: str
    data: str
    mes: str
    situacao: str
    conta: str
    detalhes: Optional[str] = None
    
    def __post_init__(self):
        """Validações básicas da entidade"""
        # Remove validações muito restritivas - permitir dados vazios da planilha
        # Se precisar de validação, fazer na camada de API/Use Cases
        pass
    
    def is_valid(self) -> bool:
        """Verifica se a transação tem os dados mínimos necessários"""
        return bool(self.tipo and self.descritivo and self.valor)
    
    def to_dict(self) -> dict:
        """Converte a entidade para dicionário"""
        return {
            "tipo": self.tipo,
            "descritivo": self.descritivo,
            "valor": self.valor,
            "data": self.data,
            "mes": self.mes,
            "detalhes": self.detalhes,
            "situacao": self.situacao,
            "conta": self.conta
        }


@dataclass
class Categoria:
    """
    Entidade que representa uma categoria
    """
    nome: str
    
    def to_dict(self) -> dict:
        """Converte a entidade para dicionário"""
        return {"nome": self.nome}


@dataclass
class Status:
    """
    Entidade que representa um status
    """
    nome: str
    tipo: str  # "RECEITA" ou "DESPESA"
    
    def to_dict(self) -> dict:
        """Converte a entidade para dicionário"""
        return {
            "nome": self.nome,
            "tipo": self.tipo
        }


@dataclass
class Conta:
    """
    Entidade que representa uma conta
    """
    nome: str
    
    def to_dict(self) -> dict:
        """Converte a entidade para dicionário"""
        return {"nome": self.nome}


@dataclass
class Cartao:
    """
    Entidade que representa um cartão
    """
    nome: str
    
    def to_dict(self) -> dict:
        """Converte a entidade para dicionário"""
        return {"nome": self.nome}
