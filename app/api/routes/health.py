"""
Rotas de health check
"""
from fastapi import APIRouter, Depends
from app.domain.schemas import HealthCheckResponse
from app.use_cases.verificar_saude import VerificarSaude
from app.api.dependencies import get_verificar_saude_use_case

router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(
    use_case: VerificarSaude = Depends(get_verificar_saude_use_case)
):
    """
    Verifica o status da API e conexão com Google Sheets
    """
    result = use_case.execute()
    return HealthCheckResponse(**result)
