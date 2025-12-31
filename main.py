"""
API Controle Financeiro - Ponto de entrada da aplicação
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import transacoes, health, configuracoes

# Configurações
settings = get_settings()

# Aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(transacoes.router)
app.include_router(health.router)
app.include_router(configuracoes.router)


@app.get("/")
async def root():
    """Endpoint raiz com informações sobre a API"""
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "endpoints": {
            "transacoes": "/api/transacoes",
            "configuracoes": "/api/configuracoes",
            "health": "/api/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
