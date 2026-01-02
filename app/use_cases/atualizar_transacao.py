"""
Caso de Uso: Atualizar Transação
"""
from app.domain.entities import Transacao
from app.data.repositories.transacao_repository_interface import TransacaoRepositoryInterface


class AtualizarTransacao:
    """Caso de uso para atualizar uma transação existente"""
    
    def __init__(self, repository: TransacaoRepositoryInterface):
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
        conta: str
    ) -> Transacao:
        """
        Atualiza uma transação
        
        Args:
            row_index: Índice da linha na planilha (>= 2)
            tipo: Tipo da transação (RECEITA ou DESPESA)
            descritivo: Descrição/categoria da transação
            valor: Valor formatado (ex: R$ 150,00)
            data: Data no formato DD/MM/YYYY
            mes: Mês por extenso (ex: Janeiro, Dezembro)
            detalhes: Detalhes adicionais
            situacao: Situação da transação
            conta: Conta relacionada
            
        Returns:
            Transacao: Entidade atualizada
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
        
        if not conta or conta.strip() == "":
            raise ValueError("Conta é obrigatória")
        
        # Cria entidade
        transacao = Transacao(
            tipo=tipo,
            descritivo=descritivo,
            valor=valor,
            data=data,
            mes=mes,
            detalhes=detalhes,
            situacao=situacao,
            conta=conta
        )
        
        # Delega para o repositório
        return self.repository.update(row_index, transacao)
