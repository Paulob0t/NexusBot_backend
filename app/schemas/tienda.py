from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# ==========================================
# TIENDA CONFIG
# ==========================================
class TiendaConfigBase(BaseModel):
    sistema: str
    hero_badge: Optional[str] = None
    hero_titulo: str
    hero_subtitulo: Optional[str] = None
    hero_cta_texto: Optional[str] = None
    hero_cta_enlace: Optional[str] = None
    whatsapp_contacto: Optional[str] = None
    whatsapp_mensaje: Optional[str] = None
    email_contacto: Optional[str] = None
    anuncio_activo: int = 0
    anuncio_texto: Optional[str] = None


class TiendaConfigUpdate(BaseModel):
    hero_badge: Optional[str] = None
    hero_titulo: Optional[str] = None
    hero_subtitulo: Optional[str] = None
    hero_cta_texto: Optional[str] = None
    hero_cta_enlace: Optional[str] = None
    whatsapp_contacto: Optional[str] = None
    whatsapp_mensaje: Optional[str] = None
    email_contacto: Optional[str] = None
    anuncio_activo: Optional[int] = None
    anuncio_texto: Optional[str] = None


class TiendaConfigResponse(TiendaConfigBase):
    id: int
    actualizado_en: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# TIENDA ITEMS (Planes / Servicios)
# ==========================================
class TiendaItemBase(BaseModel):
    sistema: str
    nombre: str
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    precio: float = 0.0
    periodo: str = "pago único"
    moneda: str = "MXN"
    caracteristicas: Optional[str] = None
    destacado: int = 0
    activo: int = 1
    orden: int = 0


class TiendaItemCreate(TiendaItemBase):
    pass


class TiendaItemUpdate(BaseModel):
    sistema: Optional[str] = None
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    periodo: Optional[str] = None
    moneda: Optional[str] = None
    caracteristicas: Optional[str] = None
    destacado: Optional[int] = None
    activo: Optional[int] = None
    orden: Optional[int] = None


class TiendaItemResponse(TiendaItemBase):
    id: int
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# TIENDA FAQS
# ==========================================
class TiendaFaqBase(BaseModel):
    sistema: str
    pregunta: str
    respuesta: str
    orden: int = 0
    activo: int = 1


class TiendaFaqCreate(TiendaFaqBase):
    pass


class TiendaFaqUpdate(BaseModel):
    sistema: Optional[str] = None
    pregunta: Optional[str] = None
    respuesta: Optional[str] = None
    orden: Optional[int] = None
    activo: Optional[int] = None


class TiendaFaqResponse(TiendaFaqBase):
    id: int
    creado_en: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
