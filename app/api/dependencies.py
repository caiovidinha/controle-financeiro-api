"""
Dependências da API - Injeção de dependências
"""
from functools import lru_cache
from app.core.config import get_settings
from app.data.repositories.google_sheets_repository import GoogleSheetsTransacaoRepository
from app.data.repositories.google_sheets_configuracao_repository import GoogleSheetsConfiguracaoRepository
from app.use_cases.listar_transacoes_paginadas import ListarTransacoesPaginadas
from app.use_cases.verificar_saude import VerificarSaude
from app.use_cases.configuracoes import (
    ListarCategorias, CriarCategoria, DeletarCategoria,
    ListarStatus,
    ListarContas, CriarConta, AtualizarConta, DeletarConta,
    ListarCartoes, CriarCartao, AtualizarCartao, DeletarCartao
)


# ==================== TRANSAÇÕES ====================

@lru_cache()
def get_transacao_repository():
    """
    Factory para obter instância do repositório de transações
    """
    settings = get_settings()
    return GoogleSheetsTransacaoRepository(settings)


def get_listar_transacoes_use_case() -> ListarTransacoesPaginadas:
    """
    Factory para obter instância do caso de uso de listar transações
    """
    repository = get_transacao_repository()
    return ListarTransacoesPaginadas(repository)


def get_verificar_saude_use_case() -> VerificarSaude:
    """
    Factory para obter instância do caso de uso de verificar saúde
    """
    repository = get_transacao_repository()
    return VerificarSaude(repository)


# ==================== CONFIGURAÇÕES ====================

@lru_cache()
def get_configuracao_repository():
    """
    Factory para obter instância do repositório de configurações
    """
    settings = get_settings()
    return GoogleSheetsConfiguracaoRepository(settings)


# Categorias
def get_listar_categorias_use_case() -> ListarCategorias:
    """Factory para listar categorias"""
    repository = get_configuracao_repository()
    return ListarCategorias(repository)


def get_criar_categoria_use_case() -> CriarCategoria:
    """Factory para criar categoria"""
    repository = get_configuracao_repository()
    return CriarCategoria(repository)


def get_deletar_categoria_use_case() -> DeletarCategoria:
    """Factory para deletar categoria"""
    repository = get_configuracao_repository()
    return DeletarCategoria(repository)


# Status
def get_listar_status_use_case() -> ListarStatus:
    """Factory para listar status"""
    repository = get_configuracao_repository()
    return ListarStatus(repository)


# Contas
def get_listar_contas_use_case() -> ListarContas:
    """Factory para listar contas"""
    repository = get_configuracao_repository()
    return ListarContas(repository)


def get_criar_conta_use_case() -> CriarConta:
    """Factory para criar conta"""
    repository = get_configuracao_repository()
    return CriarConta(repository)


def get_atualizar_conta_use_case() -> AtualizarConta:
    """Factory para atualizar conta"""
    repository = get_configuracao_repository()
    return AtualizarConta(repository)


def get_deletar_conta_use_case() -> DeletarConta:
    """Factory para deletar conta"""
    repository = get_configuracao_repository()
    return DeletarConta(repository)


# Cartões
def get_listar_cartoes_use_case() -> ListarCartoes:
    """Factory para listar cartões"""
    repository = get_configuracao_repository()
    return ListarCartoes(repository)


def get_criar_cartao_use_case() -> CriarCartao:
    """Factory para criar cartão"""
    repository = get_configuracao_repository()
    return CriarCartao(repository)


def get_atualizar_cartao_use_case() -> AtualizarCartao:
    """Factory para atualizar cartão"""
    repository = get_configuracao_repository()
    return AtualizarCartao(repository)


def get_deletar_cartao_use_case() -> DeletarCartao:
    """Factory para deletar cartão"""
    repository = get_configuracao_repository()
    return DeletarCartao(repository)
