"""
Repository para acesso aos dados da página API do Google Sheets
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Optional
from app.domain.entities import Saldo, SaldoConta
from app.core.config import Settings


class GoogleSheetsAPIRepository:
    """
    Repositório para acessar dados da página API (saldos) no Google Sheets
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.spreadsheet = None
        self.sheet_name = "API"  # Nome da página
    
    def _connect(self):
        """Conecta ao Google Sheets"""
        try:
            # Configurar credenciais
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Criar credenciais usando o mesmo padrão dos outros repositórios
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
            
            # Autorizar e abrir a planilha
            client = gspread.authorize(credentials)
            self.spreadsheet = client.open_by_key(self.settings.google_sheets_id)
            
        except Exception as e:
            print(f"Erro ao conectar ao Google Sheets: {e}")
            raise
    
    def get_saldo_geral(self) -> Saldo:
        """
        Obtém o saldo geral da célula A2 da página API
        
        Returns:
            Entidade Saldo com o valor
        """
        try:
            if not self.spreadsheet:
                self._connect()
            
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            
            # Lê a célula A2
            valor = worksheet.acell('A2').value or "R$ 0,00"
            
            return Saldo(valor=valor)
            
        except Exception as e:
            print(f"Erro ao obter saldo geral: {e}")
            raise Exception(f"Erro ao obter saldo geral: {str(e)}")
    
    def get_saldo_por_conta(self) -> List[SaldoConta]:
        """
        Obtém o saldo por conta da tabela O:P da página API
        
        Returns:
            Lista de entidades SaldoConta
        """
        try:
            if not self.spreadsheet:
                self._connect()
            
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            
            # Lê o intervalo O:P (todas as linhas das colunas O e P)
            valores = worksheet.get('O:P')
            
            if len(valores) < 2:
                return []
            
            # Ignora o cabeçalho (primeira linha)
            saldos = []
            for row in valores[1:]:
                # Ignora linhas vazias
                if not row or len(row) < 2:
                    continue
                
                conta = row[0].strip() if len(row) > 0 else ""
                saldo = row[1].strip() if len(row) > 1 else "R$ 0,00"
                
                # Adiciona apenas se a conta tiver nome
                if conta:
                    saldos.append(SaldoConta(conta=conta, saldo=saldo))
            
            return saldos
            
        except Exception as e:
            print(f"Erro ao obter saldo por conta: {e}")
            raise Exception(f"Erro ao obter saldo por conta: {str(e)}")
