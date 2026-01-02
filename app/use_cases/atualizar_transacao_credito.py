"""
Caso de Uso: Atualizar Transação de Crédito
"""
from app.domain.entities import TransacaoCredito
from app.data.repositories.transacao_credito_repository_interface import TransacaoCreditoRepositoryInterface


class AtualizarTransacaoCredito:
    """Caso de uso para atualizar uma transação de crédito existente"""
    
    def __init__(self, repository: TransacaoCreditoRepositoryInterface):
        self.repository = repository
    
    def execute(
        self,
        row_index: int,
        tipo: str,
        descritivo: str,
        valor: str,
        data: str,
        mes: str,
        detalhes: str,
        situacao: str,
        cartao: str
    ) -> TransacaoCredito:
        """
        Atualiza uma transação de crédito
        
        Args:
            row_index: Índice da linha na planilha (>= 2)
            tipo: Tipo da transação (RECEITA ou DESPESA)
            descritivo: Descrição/categoria da transação
            valor: Valor formatado (ex: R$ 85,00)
            data: Data no formato DD/MM/YYYY
            mes: Mês por extenso (ex: Janeiro, Dezembro)
            detalhes: Detalhes adicionais
            situacao: Situação da transação
            cartao: Cartão relacionado
            
        Returns:
            TransacaoCredito: Entidade atualizada
        """
        # Validações básicas
        if not tipo or tipo.strip() == "":
            raise ValueError("Tipo é obrigatório")
        
        if not descritivo or descritivo.strip() == "":
            raise ValueError("Descritivo é obrigatório")
        
        if not valor or valor.strip() == "":
            raise ValueError("Valor é obrigatório")
        
        if not data or data.strip() == "":
            raise ValueError("Data é obrigatória")
        
        if not mes or mes.strip() == "":
            raise ValueError("Mês é obrigatório")
        
        if not situacao or situacao.strip() == "":
            raise ValueError("Situação é obrigatória")
        
        if not cartao or cartao.strip() == "":
            raise ValueError("Cartão é obrigatório")
        
        # Cria entidade
        transacao = TransacaoCredito(
            tipo=tipo,
            descritivo=descritivo,
            valor=valor,
            data=data,
            mes=mes,
            detalhes=detalhes,
            situacao=situacao,
            cartao=cartao
        )
        
        # Delega para o repositório
        return self.repository.update(row_index, transacao)
