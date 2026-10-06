from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.init_db import init_db
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar Base de Datos y Sembrar Admin por defecto
    init_db()
    yield


app = FastAPI(
    title="NexusBot Enterprise CRM API",
    description="Backend API moderno para Gestión de Clientes, Dominios, Hosting y Tickets (FastAPI + SQLAlchemy + PostgreSQL)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Rutas
app.include_router(api_router, prefix="/api/v1")


@app.get("/api/health", tags=["Estado"])
def health_check():
    return {
        "status": "healthy",
        "env": settings.APP_ENV,
        "database": settings.DB_NAME,
        "db_type": settings.DB_TYPE,
        "api_version": "1.0.0"
    }


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a NexusBot API",
        "docs": "/docs",
        "health": "/api/health"
    }
