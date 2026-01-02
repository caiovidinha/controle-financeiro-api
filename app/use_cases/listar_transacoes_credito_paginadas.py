"""
Use Case: Listar transações de crédito de forma paginada
"""
from typing import Dict, Any, Optional
from app.data.repositories.transacao_credito_repository_interface import TransacaoCreditoRepositoryInterface
from app.domain.entities import TransacaoCredito


class ListarTransacoesCreditoPaginadas:
    """
    Caso de uso para listar transações de crédito com paginação e filtros
    """
    
    def __init__(self, repository: TransacaoCreditoRepositoryInterface):
        """
        Inicializa o caso de uso com um repositório
        
        Args:
            repository: Repositório de transações de crédito
        """
        self.repository = repository
    
    def execute(
        self, 
        page: int = 1, 
        page_size: int = 10,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        mes: Optional[str] = None,
        situacao: Optional[str] = None,
        cartao: Optional[str] = None,
        order_by: str = "data"
    ) -> Dict[str, Any]:
        """
        Executa o caso de uso
        
        Args:
            page: Número da página
            page_size: Tamanho da página
            tipo: Filtro por tipo (RECEITA ou DESPESA)
            categoria: Filtro por categoria/descritivo
            data_inicio: Data inicial (DD/MM/YYYY)
            data_fim: Data final (DD/MM/YYYY)
            mes: Filtro por mês
            situacao: Filtro por situação
            cartao: Filtro por cartão
            order_by: Campo para ordenação (data, tipo, categoria, valor, situacao, cartao)
            
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
        
        # Validação do tipo
        if tipo and tipo.upper() not in ["RECEITA", "DESPESA"]:
            raise ValueError("Tipo deve ser RECEITA ou DESPESA")
        
        # Validação do order_by
        valid_order_fields = ["data", "tipo", "categoria", "valor", "situacao", "cartao"]
        if order_by not in valid_order_fields:
            raise ValueError(f"order_by deve ser um dos seguintes: {', '.join(valid_order_fields)}")
        
        # Delega ao repositório com filtros
        return self.repository.get_paginated(
            page=page,
            page_size=page_size,
            tipo=tipo,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim,
            mes=mes,
            situacao=situacao,
            cartao=cartao,
            order_by=order_by
        )
