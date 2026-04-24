"""
AutoFlow AI - Main Application
Punto de entrada de la aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from database import init_db, close_db
from routers import jobs_router


# ============================================
# Lifespan events
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    
    # Startup
    print("🚀 Inicializando AutoFlow AI...")
    await init_db()
    print("✅ Base de datos inicializada")
    
    yield
    
    # Shutdown
    print("🛑 Cerrando AutoFlow AI...")
    await close_db()
    print("✅ Conexiones cerradas")


# ============================================
# Crear app FastAPI
# ============================================
app = FastAPI(
    title=settings.APP_NAME,
    description="Automatización inteligente de procesos mediante lenguaje natural",
    version=settings.APP_VERSION,
    lifespan=lifespan
)


# ============================================
# CORS Middleware
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Rutas
# ============================================
app.include_router(jobs_router)


# ============================================
# Health check
# ============================================
@app.get(
    "/health",
    tags=["health"],
    summary="Health check"
)
async def health_check():
    """
    Endpoint para verificar que la API está funcionando
    """
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get(
    "/",
    tags=["root"],
    summary="Información de la API"
)
async def root():
    """
    Información general de la API
    """
    return {
        "message": "¡Bienvenido a AutoFlow AI!",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "create_job": "POST /api/jobs/run",
            "get_status": "GET /api/jobs/status/{job_id}",
            "list_jobs": "GET /api/jobs/",
            "cancel_job": "DELETE /api/jobs/{job_id}",
            "health": "GET /health"
        }
    }


# ============================================
# Punto de entrada
# ============================================
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
