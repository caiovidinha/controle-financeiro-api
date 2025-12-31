"""
Rotas de configurações (Categorias, Status, Contas e Cartões)
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.domain.schemas import (
    CategoriaSchema, CreateCategoriaRequest,
    StatusSchema,
    ContaSchema, CreateContaRequest, UpdateContaRequest,
    CartaoSchema, CreateCartaoRequest, UpdateCartaoRequest,
    SuccessResponse
)
from app.use_cases.configuracoes import (
    ListarCategorias, CriarCategoria, DeletarCategoria,
    ListarStatus,
    ListarContas, CriarConta, AtualizarConta, DeletarConta,
    ListarCartoes, CriarCartao, AtualizarCartao, DeletarCartao
)
from app.api.dependencies import (
    get_listar_categorias_use_case, get_criar_categoria_use_case, get_deletar_categoria_use_case,
    get_listar_status_use_case,
    get_listar_contas_use_case, get_criar_conta_use_case, get_atualizar_conta_use_case, get_deletar_conta_use_case,
    get_listar_cartoes_use_case, get_criar_cartao_use_case, get_atualizar_cartao_use_case, get_deletar_cartao_use_case
)

router = APIRouter(
    prefix="/api/configuracoes",
    tags=["Configurações"]
)


# ==================== CATEGORIAS ====================

@router.get("/categorias", response_model=List[CategoriaSchema])
async def listar_categorias(
    use_case: ListarCategorias = Depends(get_listar_categorias_use_case)
):
    """Lista todas as categorias"""
    try:
        categorias = use_case.execute()
        return [CategoriaSchema(**c.to_dict()) for c in categorias]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/categorias", response_model=CategoriaSchema, status_code=status.HTTP_201_CREATED)
async def criar_categoria(
    request: CreateCategoriaRequest,
    use_case: CriarCategoria = Depends(get_criar_categoria_use_case)
):
    """Cria uma nova categoria"""
    try:
        categoria = use_case.execute(request.nome)
        return CategoriaSchema(**categoria.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/categorias/{nome}", response_model=SuccessResponse)
async def deletar_categoria(
    nome: str,
    use_case: DeletarCategoria = Depends(get_deletar_categoria_use_case)
):
    """Deleta uma categoria"""
    try:
        use_case.execute(nome)
        return SuccessResponse(message=f"Categoria '{nome}' deletada com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== STATUS ====================

@router.get("/status", response_model=List[StatusSchema])
async def listar_status(
    tipo: str = None,
    use_case: ListarStatus = Depends(get_listar_status_use_case)
):
    """
    Lista todos os status
    
    - **tipo** (opcional): Filtro por tipo - "RECEITA" ou "DESPESA"
    - Se não especificado, retorna todos os status de ambos os tipos
    """
    try:
        status_list = use_case.execute(tipo)
        return [StatusSchema(**s.to_dict()) for s in status_list]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CONTAS ====================

@router.get("/contas", response_model=List[ContaSchema])
async def listar_contas(
    use_case: ListarContas = Depends(get_listar_contas_use_case)
):
    """Lista todas as contas"""
    try:
        contas = use_case.execute()
        return [ContaSchema(**c.to_dict()) for c in contas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/contas", response_model=ContaSchema, status_code=status.HTTP_201_CREATED)
async def criar_conta(
    request: CreateContaRequest,
    use_case: CriarConta = Depends(get_criar_conta_use_case)
):
    """Cria uma nova conta"""
    try:
        conta = use_case.execute(request.nome)
        return ContaSchema(**conta.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/contas/{nome}", response_model=ContaSchema)
async def atualizar_conta(
    nome: str,
    request: UpdateContaRequest,
    use_case: AtualizarConta = Depends(get_atualizar_conta_use_case)
):
    """Atualiza o nome de uma conta existente"""
    try:
        conta = use_case.execute(nome, request.nome)
        return ContaSchema(**conta.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/contas/{nome}", response_model=SuccessResponse)
async def deletar_conta(
    nome: str,
    use_case: DeletarConta = Depends(get_deletar_conta_use_case)
):
    """Deleta uma conta"""
    try:
        use_case.execute(nome)
        return SuccessResponse(message=f"Conta '{nome}' deletada com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CARTÕES ====================

@router.get("/cartoes", response_model=List[CartaoSchema])
async def listar_cartoes(
    use_case: ListarCartoes = Depends(get_listar_cartoes_use_case)
):
    """Lista todos os cartões"""
    try:
        cartoes = use_case.execute()
        return [CartaoSchema(**c.to_dict()) for c in cartoes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cartoes", response_model=CartaoSchema, status_code=status.HTTP_201_CREATED)
async def criar_cartao(
    request: CreateCartaoRequest,
    use_case: CriarCartao = Depends(get_criar_cartao_use_case)
):
    """Cria um novo cartão"""
    try:
        cartao = use_case.execute(request.nome)
        return CartaoSchema(**cartao.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/cartoes/{nome}", response_model=CartaoSchema)
async def atualizar_cartao(
    nome: str,
    request: UpdateCartaoRequest,
    use_case: AtualizarCartao = Depends(get_atualizar_cartao_use_case)
):
    """Atualiza o nome de um cartão existente"""
    try:
        cartao = use_case.execute(nome, request.nome)
        return CartaoSchema(**cartao.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/cartoes/{nome}", response_model=SuccessResponse)
async def deletar_cartao(
    nome: str,
    use_case: DeletarCartao = Depends(get_deletar_cartao_use_case)
):
    """Deleta um cartão"""
    try:
        use_case.execute(nome)
        return SuccessResponse(message=f"Cartão '{nome}' deletado com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
