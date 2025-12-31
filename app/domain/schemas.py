"""
Schemas - Modelos de entrada/saída da API (DTOs)
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class TransacaoSchema(BaseModel):
    """Schema de uma transação para API"""
    tipo: str = Field(..., description="Tipo da transação (ex: Receita, Despesa)")
    descritivo: str = Field(..., description="Descrição da transação")
    valor: str = Field(..., description="Valor da transação")
    data: str = Field(..., description="Data da transação")
    mes: str = Field(..., description="Mês da transação")
    detalhes: Optional[str] = Field(None, description="Detalhes adicionais")
    situacao: str = Field(..., description="Situação da transação")
    conta: str = Field(..., description="Conta relacionada")

    class Config:
        json_schema_extra = {
            "example": {
                "tipo": "Despesa",
                "descritivo": "Supermercado",
                "valor": "R$ 150,00",
                "data": "15/12/2025",
                "mes": "Dezembro",
                "detalhes": "Compras mensais",
                "situacao": "Pago",
                "conta": "Conta Corrente"
            }
        }


class PaginationParams(BaseModel):
    """Parâmetros de paginação"""
    page: int = Field(1, ge=1, description="Número da página")
    page_size: int = Field(10, ge=1, le=100, description="Tamanho da página")


class TransacaoFilterParams(BaseModel):
    """Parâmetros de filtro para transações"""
    tipo: Optional[str] = Field(None, description="Tipo da transação: RECEITA ou DESPESA")
    categoria: Optional[str] = Field(None, description="Categoria/descritivo da transação")
    data_inicio: Optional[str] = Field(None, description="Data inicial (formato: DD/MM/YYYY)")
    data_fim: Optional[str] = Field(None, description="Data final (formato: DD/MM/YYYY)")
    mes: Optional[str] = Field(None, description="Mês da transação (01-Janeiro a 12-Dezembro)")
    situacao: Optional[str] = Field(None, description="Situação: 'A pagar', 'Pago', 'A receber', 'Recebido'")
    conta: Optional[str] = Field(None, description="Nome da conta")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tipo": "DESPESA",
                "categoria": "Supermercado",
                "data_inicio": "01/12/2025",
                "data_fim": "31/12/2025",
                "mes": "Dezembro",
                "situacao": "Pago",
                "conta": "Conta Corrente"
            }
        }


class PaginatedResponse(BaseModel):
    """Resposta paginada genérica"""
    total: int = Field(..., description="Total de itens")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")
    total_pages: int = Field(..., description="Total de páginas")
    items: List[TransacaoSchema] = Field(..., description="Lista de transações")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10,
                "items": []
            }
        }


class HealthCheckResponse(BaseModel):
    """Resposta do health check"""
    status: str = Field(..., description="Status da API")
    google_sheets: str = Field(..., description="Status da conexão com Google Sheets")
    error: Optional[str] = Field(None, description="Mensagem de erro, se houver")


# ==================== SCHEMAS DE CONFIGURAÇÕES ====================

class CategoriaSchema(BaseModel):
    """Schema de uma categoria"""
    nome: str = Field(..., description="Nome da categoria")
    
    class Config:
        json_schema_extra = {
            "example": {"nome": "Alimentação"}
        }


class CreateCategoriaRequest(BaseModel):
    """Request para criar uma categoria"""
    nome: str = Field(..., min_length=1, description="Nome da categoria")


class StatusSchema(BaseModel):
    """Schema de um status"""
    nome: str = Field(..., description="Nome do status")
    tipo: str = Field(..., description="Tipo do status: RECEITA ou DESPESA")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Pago",
                "tipo": "DESPESA"
            }
        }


class ContaSchema(BaseModel):
    """Schema de uma conta"""
    nome: str = Field(..., description="Nome da conta")
    
    class Config:
        json_schema_extra = {
            "example": {"nome": "Conta Corrente"}
        }


class CreateContaRequest(BaseModel):
    """Request para criar uma conta"""
    nome: str = Field(..., min_length=1, description="Nome da conta")


class UpdateContaRequest(BaseModel):
    """Request para atualizar uma conta (apenas nome)"""
    nome: str = Field(..., min_length=1, description="Novo nome da conta")


class CartaoSchema(BaseModel):
    """Schema de um cartão"""
    nome: str = Field(..., description="Nome do cartão")
    
    class Config:
        json_schema_extra = {
            "example": {"nome": "Nubank"}
        }


class CreateCartaoRequest(BaseModel):
    """Request para criar um cartão"""
    nome: str = Field(..., min_length=1, description="Nome do cartão")


class UpdateCartaoRequest(BaseModel):
    """Request para atualizar um cartão (apenas nome)"""
    nome: str = Field(..., min_length=1, description="Novo nome do cartão")


class SuccessResponse(BaseModel):
    """Resposta de sucesso genérica"""
    message: str = Field(..., description="Mensagem de sucesso")
    
    class Config:
        json_schema_extra = {
            "example": {"message": "Operação realizada com sucesso"}
        }
