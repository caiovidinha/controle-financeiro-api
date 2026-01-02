"""
Use Case: Criar uma nova transação de crédito
"""
from app.data.repositories.transacao_credito_repository_interface import TransacaoCreditoRepositoryInterface
from app.domain.entities import TransacaoCredito


class CriarTransacaoCredito:
    """
    Caso de uso para criar uma nova transação de crédito
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
        tipo: str,
        descritivo: str,
        valor: str,
        data: str,
        mes: str,
        situacao: str,
        cartao: str,
        detalhes: str = ""
    ) -> TransacaoCredito:
        """
        Executa o caso de uso
        
        Args:
            tipo: Tipo da transação
            descritivo: Descrição da transação
            valor: Valor da transação
            data: Data da transação (DD/MM/YYYY)
            mes: Mês da transação
            situacao: Situação da transação
            cartao: Cartão relacionado
            detalhes: Detalhes adicionais
            
        Returns:
            TransacaoCredito criada
        """
        # Validações de negócio
        if not tipo or not tipo.strip():
            raise ValueError("Tipo é obrigatório")
        
        if not descritivo or not descritivo.strip():
            raise ValueError("Descritivo é obrigatório")
        
        if not valor or not valor.strip():
            raise ValueError("Valor é obrigatório")
        
        if not data or not data.strip():
            raise ValueError("Data é obrigatória")
        
        if not mes or not mes.strip():
            raise ValueError("Mês é obrigatório")
        
        if not situacao or not situacao.strip():
            raise ValueError("Situação é obrigatória")
        
        if not cartao or not cartao.strip():
            raise ValueError("Cartão é obrigatório")
        
        # Cria a entidade
        transacao = TransacaoCredito(
            tipo=tipo.strip(),
            descritivo=descritivo.strip(),
            valor=valor.strip(),
            data=data.strip(),
            mes=mes.strip(),
            situacao=situacao.strip(),
            cartao=cartao.strip(),
            detalhes=detalhes.strip() if detalhes else ""
        )
        
        # Delega ao repositório
        return self.repository.create(transacao)
