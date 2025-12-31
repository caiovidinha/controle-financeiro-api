"""
Repositório de transações usando Google Sheets
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any
from app.domain.entities import Transacao
from app.data.repositories.transacao_repository_interface import TransacaoRepositoryInterface
from app.core.config import Settings


class GoogleSheetsTransacaoRepository(TransacaoRepositoryInterface):
    """
    Implementação do repositório de transações usando Google Sheets
    """
    
    def __init__(self, settings: Settings):
        """
        Inicializa o repositório com as configurações
        
        Args:
            settings: Configurações da aplicação
        """
        self.settings = settings
        self.sheets_id = settings.google_sheets_id
        self.sheet_name = settings.google_sheet_name
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
                    "private_key_id": "dummy_key_id",  # Não é necessário para autenticação
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
    
    def _get_raw_data(self) -> List[Dict[str, str]]:
        """
        Obtém dados brutos da planilha
        
        Returns:
            Lista de dicionários com os dados
        """
        try:
            if not self.spreadsheet:
                self._connect()
            
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            all_values = worksheet.get_all_values()
            
            if len(all_values) < 2:
                return []
            
            headers = all_values[0]
            
            data = []
            for row in all_values[1:]:
                # Ignora linhas completamente vazias
                if not any(cell.strip() for cell in row):
                    continue
                
                row_dict = {}
                for i, header in enumerate(headers):
                    value = row[i] if i < len(row) else ""
                    row_dict[header] = value.strip()
                
                # Adiciona apenas se tiver pelo menos TIPO, DESCRITIVO ou VALOR preenchidos
                if row_dict.get("TIPO") or row_dict.get("DESCRITIVO") or row_dict.get("VALOR"):
                    data.append(row_dict)
            
            return data
            
        except Exception as e:
            print(f"Erro ao obter dados da planilha: {e}")
            return []
    
    def _dict_to_entity(self, data: Dict[str, str]) -> Transacao:
        """
        Converte um dicionário em uma entidade Transacao
        
        Args:
            data: Dicionário com os dados
            
        Returns:
            Entidade Transacao
        """
        return Transacao(
            tipo=data.get("TIPO", ""),
            descritivo=data.get("DESCRITIVO", ""),
            valor=data.get("VALOR", ""),
            data=data.get("DATA", ""),
            mes=data.get("MÊS", ""),
            detalhes=data.get("DETALHES", ""),
            situacao=data.get("SITUAÇÃO", ""),
            conta=data.get("CONTA", "")
        )
    
    def get_all(self) -> List[Transacao]:
        """
        Obtém todas as transações
        
        Returns:
            Lista de entidades Transacao
        """
        raw_data = self._get_raw_data()
        return [self._dict_to_entity(item) for item in raw_data]
    
    def get_paginated(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Obtém transações paginadas
        
        Args:
            page: Número da página (começa em 1)
            page_size: Quantidade de itens por página
            
        Returns:
            Dicionário com dados paginados e lista de entidades
        """
        all_transacoes = self.get_all()
        total = len(all_transacoes)
        
        # Calcula índices para paginação
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Obtém apenas os itens da página atual
        page_transacoes = all_transacoes[start_idx:end_idx]
        
        # Calcula total de páginas
        total_pages = (total + page_size - 1) // page_size
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "items": page_transacoes
        }
