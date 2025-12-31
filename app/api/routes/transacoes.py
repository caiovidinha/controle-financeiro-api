"""
Rotas de transações
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from app.domain.schemas import PaginatedResponse, TransacaoSchema
from app.use_cases.listar_transacoes_paginadas import ListarTransacoesPaginadas
from app.api.dependencies import get_listar_transacoes_use_case

router = APIRouter(
    prefix="/api/transacoes",
    tags=["Transações"]
)


@router.get("", response_model=PaginatedResponse)
async def listar_transacoes(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Quantidade de itens por página"),
    use_case: ListarTransacoesPaginadas = Depends(get_listar_transacoes_use_case)
):
    """
    Lista as transações de forma paginada
    
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máximo 100)
    """
    try:
        result = use_case.execute(page=page, page_size=page_size)
        
        # Converte entidades para schemas
        transacoes_schema = [
            TransacaoSchema(**transacao.to_dict())
            for transacao in result["items"]
        ]
        
        return PaginatedResponse(
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
            items=transacoes_schema
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter transações: {str(e)}"
        )
