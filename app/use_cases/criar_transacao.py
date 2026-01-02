"""
Use Case: Criar uma nova transação
"""
from app.data.repositories.transacao_repository_interface import TransacaoRepositoryInterface
from app.domain.entities import Transacao


class CriarTransacao:
    """
    Caso de uso para criar uma nova transação
    """
    
    def __init__(self, repository: TransacaoRepositoryInterface):
        """
        Inicializa o caso de uso com um repositório
        
        Args:
            repository: Repositório de transações
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
        conta: str,
        detalhes: str = ""
    ) -> Transacao:
        """
        Executa o caso de uso
        
        Args:
            tipo: Tipo da transação
            descritivo: Descrição da transação
            valor: Valor da transação
            data: Data da transação (DD/MM/YYYY)
            mes: Mês da transação
            situacao: Situação da transação
            conta: Conta relacionada
            detalhes: Detalhes adicionais
            
        Returns:
            Transacao criada
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
        
        if not conta or not conta.strip():
            raise ValueError("Conta é obrigatória")
        
        # Cria a entidade
        transacao = Transacao(
            tipo=tipo.strip(),
            descritivo=descritivo.strip(),
            valor=valor.strip(),
            data=data.strip(),
            mes=mes.strip(),
            situacao=situacao.strip(),
            conta=conta.strip(),
            detalhes=detalhes.strip() if detalhes else ""
        )
        
        # Delega ao repositório
        return self.repository.create(transacao)
