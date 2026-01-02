"""
Rotas de transações de cartão de crédito
"""
from fastapi import APIRouter, Query, HTTPException, Depends, status
from typing import Optional
from app.domain.schemas import (
    PaginatedCreditoResponse, 
    TransacaoCreditoSchema, 
    CreateTransacaoCreditoRequest,
    UpdateTransacaoCreditoRequest,
    SuccessResponse
)
from app.use_cases.listar_transacoes_credito_paginadas import ListarTransacoesCreditoPaginadas
from app.use_cases.criar_transacao_credito import CriarTransacaoCredito
from app.use_cases.atualizar_transacao_credito import AtualizarTransacaoCredito
from app.use_cases.deletar_transacao_credito import DeletarTransacaoCredito
from app.api.dependencies import (
    get_listar_transacoes_credito_use_case, 
    get_criar_transacao_credito_use_case,
    get_atualizar_transacao_credito_use_case,
    get_deletar_transacao_credito_use_case
)

router = APIRouter(
    prefix="/api/transacoes-credito",
    tags=["Transações de Crédito"]
)


@router.get("", response_model=PaginatedCreditoResponse)
async def listar_transacoes_credito(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Quantidade de itens por página"),
    tipo: Optional[str] = Query(None, description="Filtro por tipo: RECEITA ou DESPESA"),
    categoria: Optional[str] = Query(None, description="Filtro por categoria/descritivo"),
    data_inicio: Optional[str] = Query(None, description="Data inicial (DD/MM/YYYY)"),
    data_fim: Optional[str] = Query(None, description="Data final (DD/MM/YYYY)"),
    mes: Optional[str] = Query(None, description="Filtro por mês (ex: Janeiro, Dezembro)"),
    situacao: Optional[str] = Query(None, description="Filtro por situação (ex: Pago, A pagar, Recebido, A receber)"),
    cartao: Optional[str] = Query(None, description="Filtro por cartão"),
    order_by: str = Query("data", description="Campo para ordenação: data, tipo, categoria, valor, situacao, cartao"),
    use_case: ListarTransacoesCreditoPaginadas = Depends(get_listar_transacoes_credito_use_case)
):
    """
    Lista as transações de cartão de crédito de forma paginada com filtros opcionais
    
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máximo 100)
    - **tipo**: Filtro por tipo (RECEITA ou DESPESA)
    - **categoria**: Filtro por categoria/descritivo (busca parcial)
    - **data_inicio**: Data inicial no formato DD/MM/YYYY
    - **data_fim**: Data final no formato DD/MM/YYYY
    - **mes**: Filtro por mês (ex: Janeiro, Dezembro)
    - **situacao**: Filtro por situação (ex: Pago, A pagar para DESPESA; Recebido, A receber para RECEITA)
    - **cartao**: Filtro por nome do cartão
    - **order_by**: Campo para ordenação (data, tipo, categoria, valor, situacao, cartao)
    """
    try:
        result = use_case.execute(
            page=page,
            page_size=page_size,
            tipo=tipo,
            categoria=categoria,
            data_inicio=data_inicio,
            data_fim=data_fim,
            mes=mes,
            situacao=situacao,
            cartao=cartao,
            order_by=order_by
        )
        
        # Converte entidades para schemas
        transacoes_schema = [
            TransacaoCreditoSchema(**transacao.to_dict())
            for transacao in result["items"]
        ]
        
        return PaginatedCreditoResponse(
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
            items=transacoes_schema
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=TransacaoCreditoSchema, status_code=status.HTTP_201_CREATED)
async def criar_transacao_credito(
    request: CreateTransacaoCreditoRequest,
    use_case: CriarTransacaoCredito = Depends(get_criar_transacao_credito_use_case)
):
    """
    Cria uma nova transação de cartão de crédito
    
    - **tipo**: Tipo da transação (ex: Receita, Despesa)
    - **descritivo**: Descrição da transação
    - **valor**: Valor da transação (ex: R$ 85,00)
    - **data**: Data da transação (DD/MM/YYYY)
    - **mes**: Mês da transação (ex: Janeiro, Dezembro)
    - **detalhes**: Detalhes adicionais (opcional)
    - **situacao**: Situação da transação (ex: Pago, A pagar)
    - **cartao**: Cartão relacionado
    """
    try:
        transacao = use_case.execute(
            tipo=request.tipo,
            descritivo=request.descritivo,
            valor=request.valor,
            data=request.data,
            mes=request.mes,
            situacao=request.situacao,
            cartao=request.cartao,
            detalhes=request.detalhes or ""
        )
        
        return TransacaoCreditoSchema(**transacao.to_dict())
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar transação de crédito: {str(e)}"
        )


@router.put("/{row_index}", response_model=TransacaoCreditoSchema)
async def atualizar_transacao_credito(
    row_index: int,
    request: UpdateTransacaoCreditoRequest,
    use_case: AtualizarTransacaoCredito = Depends(get_atualizar_transacao_credito_use_case)
):
    """
    Atualiza uma transação de cartão de crédito existente
    
    - **row_index**: Índice da linha na planilha (>= 2, pois linha 1 é o cabeçalho)
    - **tipo**: Tipo da transação (ex: Receita, Despesa)
    - **descritivo**: Descrição da transação
    - **valor**: Valor da transação (ex: R$ 85,00)
    - **data**: Data da transação (DD/MM/YYYY)
    - **mes**: Mês da transação (ex: Janeiro, Dezembro)
    - **detalhes**: Detalhes adicionais (opcional)
    - **situacao**: Situação da transação (ex: Pago, A pagar)
    - **cartao**: Cartão relacionado
    """
    try:
        transacao = use_case.execute(
            row_index=row_index,
            tipo=request.tipo,
            descritivo=request.descritivo,
            valor=request.valor,
            data=request.data,
            mes=request.mes,
            situacao=request.situacao,
            cartao=request.cartao,
            detalhes=request.detalhes or ""
        )
        
        return TransacaoCreditoSchema(**transacao.to_dict())
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar transação de crédito: {str(e)}"
        )


@router.delete("/{row_index}", response_model=SuccessResponse)
async def deletar_transacao_credito(
    row_index: int,
    use_case: DeletarTransacaoCredito = Depends(get_deletar_transacao_credito_use_case)
):
    """
    Deleta uma transação de cartão de crédito
    
    - **row_index**: Índice da linha na planilha (>= 2, pois linha 1 é o cabeçalho)
    """
    try:
        use_case.execute(row_index=row_index)
        
        return SuccessResponse(message=f"Transação de crédito na linha {row_index} deletada com sucesso")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar transação de crédito: {str(e)}"
        )
