"""
Use Cases para gerenciamento de configurações
"""
from typing import List
from app.data.repositories.configuracao_repository_interface import ConfiguracaoRepositoryInterface
from app.domain.entities import Categoria, Status, Conta, Cartao


# ==================== CATEGORIAS ====================

class ListarCategorias:
    """Caso de uso para listar todas as categorias"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self) -> List[Categoria]:
        """Executa o caso de uso"""
        return self.repository.get_all_categorias()


class CriarCategoria:
    """Caso de uso para criar uma categoria"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome: str) -> Categoria:
        """Executa o caso de uso"""
        if not nome or not nome.strip():
            raise ValueError("Nome da categoria é obrigatório")
        
        # Verifica se já existe
        categorias = self.repository.get_all_categorias()
        if any(c.nome == nome for c in categorias):
            raise ValueError(f"Categoria '{nome}' já existe")
        
        return self.repository.create_categoria(nome.strip())


class DeletarCategoria:
    """Caso de uso para deletar uma categoria"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome: str) -> bool:
        """Executa o caso de uso"""
        if not nome or not nome.strip():
            raise ValueError("Nome da categoria é obrigatório")
        
        deleted = self.repository.delete_categoria(nome.strip())
        if not deleted:
            raise ValueError(f"Categoria '{nome}' não encontrada")
        
        return True


# ==================== STATUS ====================

class ListarStatus:
    """Caso de uso para listar todos os status"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, tipo: str = None) -> List[Status]:
        """
        Executa o caso de uso
        
        Args:
            tipo: Filtro opcional por tipo ("RECEITA" ou "DESPESA")
        """
        if tipo and tipo.upper() not in ["RECEITA", "DESPESA"]:
            raise ValueError("Tipo deve ser 'RECEITA' ou 'DESPESA'")
        
        return self.repository.get_all_status(tipo)


# ==================== CONTAS ====================

class ListarContas:
    """Caso de uso para listar todas as contas"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self) -> List[Conta]:
        """Executa o caso de uso"""
        return self.repository.get_all_contas()


class CriarConta:
    """Caso de uso para criar uma conta"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome: str) -> Conta:
        """Executa o caso de uso"""
        if not nome or not nome.strip():
            raise ValueError("Nome da conta é obrigatório")
        
        # Verifica se já existe
        contas = self.repository.get_all_contas()
        if any(c.nome == nome for c in contas):
            raise ValueError(f"Conta '{nome}' já existe")
        
        return self.repository.create_conta(nome.strip())


class AtualizarConta:
    """Caso de uso para atualizar uma conta"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome_antigo: str, nome_novo: str) -> Conta:
        """Executa o caso de uso"""
        if not nome_antigo or not nome_antigo.strip():
            raise ValueError("Nome antigo da conta é obrigatório")
        
        if not nome_novo or not nome_novo.strip():
            raise ValueError("Nome novo da conta é obrigatório")
        
        # Verifica se o novo nome já existe
        contas = self.repository.get_all_contas()
        if any(c.nome == nome_novo for c in contas):
            raise ValueError(f"Conta '{nome_novo}' já existe")
        
        return self.repository.update_conta(nome_antigo.strip(), nome_novo.strip())


class DeletarConta:
    """Caso de uso para deletar uma conta"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome: str) -> bool:
        """Executa o caso de uso"""
        if not nome or not nome.strip():
            raise ValueError("Nome da conta é obrigatório")
        
        deleted = self.repository.delete_conta(nome.strip())
        if not deleted:
            raise ValueError(f"Conta '{nome}' não encontrada")
        
        return True


# ==================== CARTÕES ====================

class ListarCartoes:
    """Caso de uso para listar todos os cartões"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self) -> List[Cartao]:
        """Executa o caso de uso"""
        return self.repository.get_all_cartoes()


class CriarCartao:
    """Caso de uso para criar um cartão"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome: str) -> Cartao:
        """Executa o caso de uso"""
        if not nome or not nome.strip():
            raise ValueError("Nome do cartão é obrigatório")
        
        # Verifica se já existe
        cartoes = self.repository.get_all_cartoes()
        if any(c.nome == nome for c in cartoes):
            raise ValueError(f"Cartão '{nome}' já existe")
        
        return self.repository.create_cartao(nome.strip())


class AtualizarCartao:
    """Caso de uso para atualizar um cartão"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome_antigo: str, nome_novo: str) -> Cartao:
        """Executa o caso de uso"""
        if not nome_antigo or not nome_antigo.strip():
            raise ValueError("Nome antigo do cartão é obrigatório")
        
        if not nome_novo or not nome_novo.strip():
            raise ValueError("Nome novo do cartão é obrigatório")
        
        # Verifica se o novo nome já existe
        cartoes = self.repository.get_all_cartoes()
        if any(c.nome == nome_novo for c in cartoes):
            raise ValueError(f"Cartão '{nome_novo}' já existe")
        
        return self.repository.update_cartao(nome_antigo.strip(), nome_novo.strip())


class DeletarCartao:
    """Caso de uso para deletar um cartão"""
    
    def __init__(self, repository: ConfiguracaoRepositoryInterface):
        self.repository = repository
    
    def execute(self, nome: str) -> bool:
        """Executa o caso de uso"""
        if not nome or not nome.strip():
            raise ValueError("Nome do cartão é obrigatório")
        
        deleted = self.repository.delete_cartao(nome.strip())
        if not deleted:
            raise ValueError(f"Cartão '{nome}' não encontrado")
        
        return True
