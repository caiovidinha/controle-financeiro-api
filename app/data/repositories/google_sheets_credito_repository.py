"""
Repositório Google Sheets para transações de cartão de crédito
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import Settings
from app.data.repositories.transacao_credito_repository_interface import TransacaoCreditoRepositoryInterface
from app.domain.entities import TransacaoCredito


class GoogleSheetsCreditoRepository(TransacaoCreditoRepositoryInterface):
    """
    Implementação do repositório usando Google Sheets como fonte de dados
    """
    
    def __init__(self, settings: Settings):
        """
        Inicializa o repositório com as configurações
        
        Args:
            settings: Configurações da aplicação
        """
        self.settings = settings
        self.sheets_id = settings.google_sheets_id
        self.sheet_name = "Extrato Crédito"
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
            Lista de dicionários com os dados (incluindo row_index)
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
            for idx, row in enumerate(all_values[1:], start=2):  # start=2 porque linha 1 é header
                # Ignora linhas completamente vazias
                if not any(cell.strip() for cell in row):
                    continue
                
                row_dict = {}
                for i, header in enumerate(headers):
                    value = row[i] if i < len(row) else ""
                    row_dict[header] = value.strip()
                
                # Adiciona apenas se tiver pelo menos TIPO, DESCRITIVO ou VALOR preenchidos
                if row_dict.get("TIPO") or row_dict.get("DESCRITIVO") or row_dict.get("VALOR"):
                    row_dict["_row_index"] = idx  # Armazena o índice da linha
                    data.append(row_dict)
            
            return data
            
        except Exception as e:
            print(f"Erro ao obter dados da planilha: {e}")
            return []
    
    def _dict_to_entity(self, data: Dict[str, str]) -> TransacaoCredito:
        """
        Converte um dicionário em uma entidade TransacaoCredito
        
        Args:
            data: Dicionário com os dados (pode incluir _row_index)
            
        Returns:
            Entidade TransacaoCredito
        """
        return TransacaoCredito(
            tipo=data.get("TIPO", ""),
            descritivo=data.get("DESCRITIVO", ""),
            valor=data.get("VALOR", ""),
            data=data.get("DATA", ""),
            mes=data.get("MÊS", ""),
            detalhes=data.get("DETALHES", ""),
            situacao=data.get("SITUAÇÃO", ""),
            cartao=data.get("CARTÃO", ""),
            row_index=data.get("_row_index")
        )
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Converte string de data DD/MM/YYYY para datetime
        
        Args:
            date_str: String da data
            
        Returns:
            Objeto datetime
        """
        try:
            return datetime.strptime(date_str.strip(), "%d/%m/%Y")
        except:
            return None
    
    def _apply_filters(
        self,
        transacoes: List[TransacaoCredito],
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        mes: Optional[str] = None,
        situacao: Optional[str] = None,
        cartao: Optional[str] = None,
        order_by: str = "data"
    ) -> List[TransacaoCredito]:
        """
        Aplica filtros à lista de transações
        
        Args:
            transacoes: Lista de transações
            tipo: Filtro por tipo (RECEITA ou DESPESA)
            categoria: Filtro por categoria/descritivo
            data_inicio: Data inicial (DD/MM/YYYY)
            data_fim: Data final (DD/MM/YYYY)
            mes: Filtro por mês
            situacao: Filtro por situação
            cartao: Filtro por cartão
            order_by: Campo para ordenação (data, tipo, categoria, valor, situacao, cartao)
            
        Returns:
            Lista filtrada de transações
        """
        filtered = transacoes
        
        # Filtro por tipo
        if tipo:
            tipo_upper = tipo.upper()
            filtered = [t for t in filtered if t.tipo.upper() == tipo_upper]
        
        # Filtro por categoria/descritivo (case-insensitive, contains)
        if categoria:
            categoria_lower = categoria.lower()
            filtered = [t for t in filtered if categoria_lower in t.descritivo.lower()]
        
        # Filtro por data (intervalo)
        if data_inicio or data_fim:
            date_filtered = []
            dt_inicio = self._parse_date(data_inicio) if data_inicio else None
            dt_fim = self._parse_date(data_fim) if data_fim else None
            
            for t in filtered:
                dt_transacao = self._parse_date(t.data)
                if dt_transacao:
                    if dt_inicio and dt_transacao < dt_inicio:
                        continue
                    if dt_fim and dt_transacao > dt_fim:
                        continue
                    date_filtered.append(t)
            filtered = date_filtered
        
        # Filtro por mês (case-insensitive)
        if mes:
            mes_lower = mes.lower()
            filtered = [t for t in filtered if mes_lower in t.mes.lower()]
        
        # Filtro por situação (case-insensitive)
        if situacao:
            situacao_lower = situacao.lower()
            filtered = [t for t in filtered if situacao_lower in t.situacao.lower()]
        
        # Filtro por cartão (case-insensitive)
        if cartao:
            cartao_lower = cartao.lower()
            filtered = [t for t in filtered if cartao_lower in t.cartao.lower()]
        
        # Ordenação
        filtered = self._sort_transacoes(filtered, order_by)
        
        return filtered
    
    def _sort_transacoes(self, transacoes: List[TransacaoCredito], order_by: str) -> List[TransacaoCredito]:
        """
        Ordena transações pelo campo especificado
        
        Args:
            transacoes: Lista de transações
            order_by: Campo para ordenação (data, tipo, categoria, valor, situacao, cartao)
            
        Returns:
            Lista ordenada
        """
        if order_by == "data":
            # Ordena por data (mais recente primeiro)
            return sorted(
                transacoes,
                key=lambda t: self._parse_date(t.data) or datetime.min,
                reverse=True
            )
        elif order_by == "tipo":
            return sorted(transacoes, key=lambda t: t.tipo.lower())
        elif order_by == "categoria":
            return sorted(transacoes, key=lambda t: t.descritivo.lower())
        elif order_by == "valor":
            # Remove formatação e converte para float
            def parse_valor(valor_str: str) -> float:
                try:
                    # Remove R$, espaços e converte vírgula para ponto
                    clean = valor_str.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                    return float(clean)
                except:
                    return 0.0
            return sorted(transacoes, key=lambda t: parse_valor(t.valor), reverse=True)
        elif order_by == "situacao":
            return sorted(transacoes, key=lambda t: t.situacao.lower())
        elif order_by == "cartao":
            return sorted(transacoes, key=lambda t: t.cartao.lower())
        else:
            # Se order_by inválido, retorna por data
            return sorted(
                transacoes,
                key=lambda t: self._parse_date(t.data) or datetime.min,
                reverse=True
            )
    
    def get_all(
        self,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        mes: Optional[str] = None,
        situacao: Optional[str] = None,
        cartao: Optional[str] = None,
        order_by: str = "data"
    ) -> List[TransacaoCredito]:
        """
        Obtém todas as transações com filtros opcionais
        
        Args:
            tipo: Filtro por tipo (RECEITA ou DESPESA)
            categoria: Filtro por categoria/descritivo
            data_inicio: Data inicial (DD/MM/YYYY)
            data_fim: Data final (DD/MM/YYYY)
            mes: Filtro por mês
            situacao: Filtro por situação
            cartao: Filtro por cartão
            order_by: Campo para ordenação (data, tipo, categoria, valor, situacao, cartao)
        
        Returns:
            Lista de entidades TransacaoCredito
        """
        raw_data = self._get_raw_data()
        all_transacoes = [self._dict_to_entity(item) for item in raw_data]
        return self._apply_filters(
            all_transacoes,
            tipo=tipo,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim,
            mes=mes,
            situacao=situacao,
            cartao=cartao,
            order_by=order_by
        )
    
    def get_paginated(
        self, 
        page: int = 1, 
        page_size: int = 10,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        mes: Optional[str] = None,
        situacao: Optional[str] = None,
        cartao: Optional[str] = None,
        order_by: str = "data"
    ) -> Dict[str, Any]:
        """
        Obtém transações paginadas com filtros opcionais
        
        Args:
            page: Número da página (começa em 1)
            page_size: Quantidade de itens por página
            tipo: Filtro por tipo (RECEITA ou DESPESA)
            categoria: Filtro por categoria/descritivo
            data_inicio: Data inicial (DD/MM/YYYY)
            data_fim: Data final (DD/MM/YYYY)
            mes: Filtro por mês
            situacao: Filtro por situação
            cartao: Filtro por cartão
            order_by: Campo para ordenação (data, tipo, categoria, valor, situacao, cartao)
            
        Returns:
            Dicionário com dados paginados e lista de entidades
        """
        all_transacoes = self.get_all(
            tipo=tipo,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim,
            mes=mes,
            situacao=situacao,
            cartao=cartao,
            order_by=order_by
        )
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
            "total_pages": total_pages if total > 0 else 1,
            "items": page_transacoes
        }
    
    def create(self, transacao: TransacaoCredito) -> TransacaoCredito:
        """
        Cria uma nova transação de crédito na planilha
        
        Args:
            transacao: Entidade TransacaoCredito a ser criada
            
        Returns:
            Entidade TransacaoCredito criada
        """
        try:
            if not self.spreadsheet:
                self._connect()
            
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            
            # Prepara linha para inserção
            nova_linha = [
                transacao.tipo,
                transacao.descritivo,
                transacao.valor,
                transacao.data,
                transacao.mes,
                transacao.detalhes or "",
                transacao.situacao,
                transacao.cartao
            ]
            
            # Adiciona ao final da planilha
            worksheet.append_row(nova_linha)
            
            return transacao
            
        except Exception as e:
            print(f"Erro ao criar transação de crédito: {e}")
            raise Exception(f"Erro ao criar transação de crédito: {str(e)}")
    
    def update(self, row_index: int, transacao: TransacaoCredito) -> TransacaoCredito:
        """
        Atualiza uma transação de crédito existente na planilha
        
        Args:
            row_index: Índice da linha (2 = primeira linha de dados, pois linha 1 é o cabeçalho)
            transacao: Entidade TransacaoCredito com os novos dados
            
        Returns:
            Entidade TransacaoCredito atualizada
        """
        try:
            if not self.spreadsheet:
                self._connect()
            
            if row_index < 2:
                raise ValueError("Índice da linha deve ser >= 2 (linha 1 é o cabeçalho)")
            
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            
            # Prepara valores para atualização
            valores = [
                transacao.tipo,
                transacao.descritivo,
                transacao.valor,
                transacao.data,
                transacao.mes,
                transacao.detalhes or "",
                transacao.situacao,
                transacao.cartao
            ]
            
            # Atualiza a linha inteira (colunas A até H)
            range_name = f'A{row_index}:H{row_index}'
            worksheet.update(range_name, [valores])
            
            return transacao
            
        except Exception as e:
            print(f"Erro ao atualizar transação de crédito: {e}")
            raise Exception(f"Erro ao atualizar transação de crédito: {str(e)}")
    
    def delete(self, row_index: int) -> bool:
        """
        Deleta uma transação de crédito da planilha
        
        Args:
            row_index: Índice da linha (2 = primeira linha de dados, pois linha 1 é o cabeçalho)
            
        Returns:
            True se deletou com sucesso
        """
        try:
            if not self.spreadsheet:
                self._connect()
            
            if row_index < 2:
                raise ValueError("Índice da linha deve ser >= 2 (linha 1 é o cabeçalho)")
            
            worksheet = self.spreadsheet.worksheet(self.sheet_name)
            worksheet.delete_rows(row_index)
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar transação de crédito: {e}")
            raise Exception(f"Erro ao deletar transação de crédito: {str(e)}")
