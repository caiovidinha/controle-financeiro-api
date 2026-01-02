"""
Repositório de configurações usando Google Sheets
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Optional
from app.domain.entities import Categoria, Status, Conta, Cartao, Mes
from app.data.repositories.configuracao_repository_interface import ConfiguracaoRepositoryInterface
from app.core.config import Settings


class GoogleSheetsConfiguracaoRepository(ConfiguracaoRepositoryInterface):
    """
    Implementação do repositório de configurações usando Google Sheets
    """
    
    def __init__(self, settings: Settings):
        """
        Inicializa o repositório com as configurações
        
        Args:
            settings: Configurações da aplicação
        """
        self.settings = settings
        self.sheets_id = settings.google_sheets_id
        self.sheet_name = "Configurações"  # Nome da aba de configurações
        self.spreadsheet = None
        self._connect()
    
    def _connect(self):
        """Conecta ao Google Sheets"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                {
                    "type": "service_account",
                    "project_id": "controle-financeiro-450717",
                    "private_key_id": "dummy_key_id",
                    "private_key": self.settings.google_private_key.replace('\\n', '\n'),
                    "client_email": self.settings.google_service_account_email,
                    "client_id": "",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{self.settings.google_service_account_email.replace('@', '%40')}"
                },
                scope
            )
            
            client = gspread.authorize(credentials)
            self.spreadsheet = client.open_by_key(self.sheets_id)
            
        except Exception as e:
            print(f"Erro ao conectar ao Google Sheets: {e}")
            raise
    
    def _get_worksheet(self):
        """Obtém a worksheet de configurações"""
        if not self.spreadsheet:
            self._connect()
        return self.spreadsheet.worksheet(self.sheet_name)
    
    def _get_column_values(self, col_letter: str) -> List[str]:
        """
        Obtém todos os valores de uma coluna (exceto o cabeçalho)
        
        Args:
            col_letter: Letra da coluna (A, B, C, D)
            
        Returns:
            Lista de valores não vazios
        """
        worksheet = self._get_worksheet()
        values = worksheet.col_values(ord(col_letter) - ord('A') + 1)
        # Remove o cabeçalho e valores vazios
        return [v.strip() for v in values[1:] if v.strip()]
    
    def _append_to_column(self, col_letter: str, value: str):
        """
        Adiciona um valor ao final de uma coluna
        
        Args:
            col_letter: Letra da coluna
            value: Valor a adicionar
        """
        worksheet = self._get_worksheet()
        col_num = ord(col_letter) - ord('A') + 1
        values = worksheet.col_values(col_num)
        next_row = len(values) + 1
        worksheet.update_cell(next_row, col_num, value)
    
    def _delete_from_column(self, col_letter: str, value: str) -> bool:
        """
        Deleta um valor de uma coluna
        
        Args:
            col_letter: Letra da coluna
            value: Valor a deletar
            
        Returns:
            True se deletou, False se não encontrou
        """
        worksheet = self._get_worksheet()
        col_num = ord(col_letter) - ord('A') + 1
        
        try:
            cell = worksheet.find(value, in_column=col_num)
            if cell and cell.row > 1:  # Não deletar o cabeçalho
                worksheet.update_cell(cell.row, col_num, "")
                return True
        except:
            pass
        return False
    
    def _update_in_column(self, col_letter: str, old_value: str, new_value: str) -> bool:
        """
        Atualiza um valor em uma coluna
        
        Args:
            col_letter: Letra da coluna
            old_value: Valor antigo
            new_value: Novo valor
            
        Returns:
            True se atualizou, False se não encontrou
        """
        worksheet = self._get_worksheet()
        col_num = ord(col_letter) - ord('A') + 1
        
        try:
            cell = worksheet.find(old_value, in_column=col_num)
            if cell and cell.row > 1:
                worksheet.update_cell(cell.row, col_num, new_value)
                return True
        except:
            pass
        return False
    
    # ==================== CATEGORIAS ====================
    
    def get_all_categorias(self) -> List[Categoria]:
        """Obtém todas as categorias (coluna A)"""
        values = self._get_column_values('A')
        return [Categoria(nome=v) for v in values]
    
    def create_categoria(self, nome: str) -> Categoria:
        """Cria uma nova categoria"""
        self._append_to_column('A', nome)
        return Categoria(nome=nome)
    
    def delete_categoria(self, nome: str) -> bool:
        """Deleta uma categoria"""
        return self._delete_from_column('A', nome)
    
    # ==================== STATUS ====================
    
    def get_all_status(self, tipo: str = None) -> List[Status]:
        """
        Obtém todos os status
        
        Args:
            tipo: Filtro opcional por tipo ("RECEITA" ou "DESPESA")
            
        Returns:
            Lista de status filtrados por tipo (se especificado)
        """
        status_list = []
        
        # Coluna B - Status de Receita
        if tipo is None or tipo.upper() == "RECEITA":
            receitas = self._get_column_values('B')
            status_list.extend([Status(nome=v, tipo="RECEITA") for v in receitas])
        
        # Coluna C - Status de Despesa  
        if tipo is None or tipo.upper() == "DESPESA":
            despesas = self._get_column_values('C')
            status_list.extend([Status(nome=v, tipo="DESPESA") for v in despesas])
        
        return status_list
    
    # ==================== MESES ====================
    
    def get_all_meses(self) -> List[Mes]:
        """
        Obtém todos os meses da coluna G
        
        Returns:
            Lista de meses
        """
        meses = self._get_column_values('G')
        return [Mes(nome=m) for m in meses]
    
    # ==================== CONTAS ====================
    
    def get_all_contas(self) -> List[Conta]:
        """Obtém todas as contas (coluna D)"""
        values = self._get_column_values('D')
        return [Conta(nome=v) for v in values]
    
    def create_conta(self, nome: str) -> Conta:
        """Cria uma nova conta"""
        self._append_to_column('D', nome)
        return Conta(nome=nome)
    
    def update_conta(self, nome_antigo: str, nome_novo: str) -> Conta:
        """Atualiza o nome de uma conta existente"""
        success = self._update_in_column('D', nome_antigo, nome_novo)
        if not success:
            raise ValueError(f"Conta '{nome_antigo}' não encontrada")
        return Conta(nome=nome_novo)
    
    def delete_conta(self, nome: str) -> bool:
        """Deleta uma conta"""
        return self._delete_from_column('D', nome)
    
    # ==================== CARTÕES ====================
    
    def get_all_cartoes(self) -> List[Cartao]:
        """Obtém todos os cartões (coluna E)"""
        values = self._get_column_values('E')
        return [Cartao(nome=v) for v in values]
    
    def create_cartao(self, nome: str) -> Cartao:
        """Cria um novo cartão"""
        self._append_to_column('E', nome)
        return Cartao(nome=nome)
    
    def update_cartao(self, nome_antigo: str, nome_novo: str) -> Cartao:
        """Atualiza o nome de um cartão existente"""
        success = self._update_in_column('E', nome_antigo, nome_novo)
        if not success:
            raise ValueError(f"Cartão '{nome_antigo}' não encontrado")
        return Cartao(nome=nome_novo)
    
    def delete_cartao(self, nome: str) -> bool:
        """Deleta um cartão"""
        return self._delete_from_column('E', nome)
