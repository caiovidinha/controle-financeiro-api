"""
Dependências da API - Injeção de dependências
"""
from functools import lru_cache
from app.core.config import get_settings
from app.data.repositories.google_sheets_repository import GoogleSheetsTransacaoRepository
from app.data.repositories.google_sheets_credito_repository import GoogleSheetsCreditoRepository
from app.data.repositories.google_sheets_configuracao_repository import GoogleSheetsConfiguracaoRepository
from app.data.repositories.google_sheets_api_repository import GoogleSheetsAPIRepository
from app.use_cases.listar_transacoes_paginadas import ListarTransacoesPaginadas
from app.use_cases.criar_transacao import CriarTransacao
from app.use_cases.atualizar_transacao import AtualizarTransacao
from app.use_cases.deletar_transacao import DeletarTransacao
from app.use_cases.listar_transacoes_credito_paginadas import ListarTransacoesCreditoPaginadas
from app.use_cases.criar_transacao_credito import CriarTransacaoCredito
from app.use_cases.atualizar_transacao_credito import AtualizarTransacaoCredito
from app.use_cases.deletar_transacao_credito import DeletarTransacaoCredito
from app.use_cases.verificar_saude import VerificarSaude
from app.use_cases.saldos import ObterSaldoGeral, ObterSaldoPorConta
from app.use_cases.configuracoes import (
    ListarCategorias, CriarCategoria, DeletarCategoria,
    ListarStatus, ListarMeses,
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


def get_criar_transacao_use_case() -> CriarTransacao:
    """
    Factory para obter instância do caso de uso de criar transação
    """
    repository = get_transacao_repository()
    return CriarTransacao(repository)


def get_atualizar_transacao_use_case() -> AtualizarTransacao:
    """
    Factory para obter instância do caso de uso de atualizar transação
    """
    repository = get_transacao_repository()
    return AtualizarTransacao(repository)


def get_deletar_transacao_use_case() -> DeletarTransacao:
    """
    Factory para obter instância do caso de uso de deletar transação
    """
    repository = get_transacao_repository()
    return DeletarTransacao(repository)


def get_verificar_saude_use_case() -> VerificarSaude:
    """
    Factory para obter instância do caso de uso de verificar saúde
    """
    repository = get_transacao_repository()
    return VerificarSaude(repository)


# ==================== TRANSAÇÕES DE CRÉDITO ====================

@lru_cache()
def get_transacao_credito_repository():
    """
    Factory para obter instância do repositório de transações de crédito
    """
    settings = get_settings()
    return GoogleSheetsCreditoRepository(settings)


def get_listar_transacoes_credito_use_case() -> ListarTransacoesCreditoPaginadas:
    """
    Factory para obter instância do caso de uso de listar transações de crédito
    """
    repository = get_transacao_credito_repository()
    return ListarTransacoesCreditoPaginadas(repository)


def get_criar_transacao_credito_use_case() -> CriarTransacaoCredito:
    """
    Factory para obter instância do caso de uso de criar transação de crédito
    """
    repository = get_transacao_credito_repository()
    return CriarTransacaoCredito(repository)


def get_atualizar_transacao_credito_use_case() -> AtualizarTransacaoCredito:
    """
    Factory para obter instância do caso de uso de atualizar transação de crédito
    """
    repository = get_transacao_credito_repository()
    return AtualizarTransacaoCredito(repository)


def get_deletar_transacao_credito_use_case() -> DeletarTransacaoCredito:
    """
    Factory para obter instância do caso de uso de deletar transação de crédito
    """
    repository = get_transacao_credito_repository()
    return DeletarTransacaoCredito(repository)


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


# Meses
def get_listar_meses_use_case() -> ListarMeses:
    """Factory para listar meses"""
    repository = get_configuracao_repository()
    return ListarMeses(repository)


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


# ==================== SALDOS ====================

@lru_cache()
def get_api_repository():
    """
    Factory para obter instância do repositório da página API
    """
    settings = get_settings()
    return GoogleSheetsAPIRepository(settings)


def get_obter_saldo_geral_use_case() -> ObterSaldoGeral:
    """Factory para obter saldo geral"""
    repository = get_api_repository()
    return ObterSaldoGeral(repository)


def get_obter_saldo_por_conta_use_case() -> ObterSaldoPorConta:
    """Factory para obter saldo por conta"""
    repository = get_api_repository()
    return ObterSaldoPorConta(repository)
