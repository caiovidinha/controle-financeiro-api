"""
Rotas de saldos
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.domain.schemas import SaldoSchema, SaldoContaSchema
from app.use_cases.saldos import ObterSaldoGeral, ObterSaldoPorConta
from app.api.dependencies import get_obter_saldo_geral_use_case, get_obter_saldo_por_conta_use_case

router = APIRouter(
    prefix="/api/saldos",
    tags=["Saldos"]
)


@router.get("", response_model=SaldoSchema)
async def obter_saldo_geral(
    use_case: ObterSaldoGeral = Depends(get_obter_saldo_geral_use_case)
):
    """
    Retorna o saldo geral da célula A2 da página API
    
    Retorna o valor total consolidado de todas as contas.
    """
    try:
        saldo = use_case.execute()
        return SaldoSchema(**saldo.to_dict())
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter saldo geral: {str(e)}"
        )


@router.get("/contas", response_model=List[SaldoContaSchema])
async def obter_saldo_por_conta(
    use_case: ObterSaldoPorConta = Depends(get_obter_saldo_por_conta_use_case)
):
    """
    Retorna o saldo de cada conta (tabela O:P da página API)
    
    Lista todas as contas com seus respectivos saldos.
    """
    try:
        saldos = use_case.execute()
        return [SaldoContaSchema(**saldo.to_dict()) for saldo in saldos]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter saldo por conta: {str(e)}"
        )
