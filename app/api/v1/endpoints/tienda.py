from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.auth import UserProfile
from app.models.tienda import TiendaConfig, TiendaItem, TiendaFaq
from app.schemas.tienda import (
    TiendaConfigResponse,
    TiendaConfigUpdate,
    TiendaItemResponse,
    TiendaItemCreate,
    TiendaItemUpdate,
    TiendaFaqResponse,
    TiendaFaqCreate,
    TiendaFaqUpdate,
)

router = APIRouter()


def ensure_admin(current_user: UserProfile):
    if current_user.id_tipo_usuario < 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador para realizar esta acción."
        )


def get_default_config(sistema: str) -> TiendaConfig:
    if sistema == "hostingpro":
        return TiendaConfig(
            sistema="hostingpro",
            hero_badge="Infraestructura Cloud & Hosting 2026",
            hero_titulo="Servidores de Alto Rendimiento y Bots Inteligentes",
            hero_subtitulo="Alojamiento web ultra rápido, discos NVMe, soporte 24/7 y automatizaciones para escalar tu infraestructura digital.",
            hero_cta_texto="Ver Planes de Hosting",
            hero_cta_enlace="#catalogo",
            whatsapp_contacto="5215500000000",
            whatsapp_mensaje="Hola, me gustaría cotizar un servidor o plan de hosting en Puvnext Bot.",
            email_contacto="contacto@puvnex.io",
            anuncio_activo=1,
            anuncio_texto="🔥 20% de descuento en la contratación anual de cualquier plan Cloud.",
        )
    else:
        return TiendaConfig(
            sistema="conlineweb",
            hero_badge="Soluciones Digitales & Desarrollo Web",
            hero_titulo="Diseño Web Profesional y Tiendas Online de Alto Impacto",
            hero_subtitulo="Desarrollamos la identidad digital de tu empresa con tecnologías modernas, velocidad óptima y conversión garantizada.",
            hero_cta_texto="Explorar Paquetes Web",
            hero_cta_enlace="#catalogo",
            whatsapp_contacto="5215500000000",
            whatsapp_mensaje="Hola, me gustaría cotizar un desarrollo web para mi empresa en Puvnext Web.",
            email_contacto="ventas@puvnex.io",
            anuncio_activo=1,
            anuncio_texto="🚀 ¡Lanza tu sitio web este mes con dominio y hosting incluido!",
        )


# ==========================================
# ENDPOINTS CONFIGURACIÓN DE TIENDA
# ==========================================
@router.get("/config", response_model=TiendaConfigResponse)
def get_tienda_config(
    sistema: str = Query(..., description="Sistema ('conlineweb' o 'hostingpro')"),
    db: Session = Depends(get_db)
):
    """Obtiene la configuración activa de la tienda para el sistema indicado."""
    config = db.query(TiendaConfig).filter(TiendaConfig.sistema == sistema).first()
    if not config:
        config = get_default_config(sistema)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


@router.put("/config", response_model=TiendaConfigResponse)
def update_tienda_config(
    payload: TiendaConfigUpdate,
    sistema: str = Query(..., description="Sistema ('conlineweb' o 'hostingpro')"),
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Actualiza la configuración y datos del Hero/Contacto de la tienda."""
    ensure_admin(current_user)
    config = db.query(TiendaConfig).filter(TiendaConfig.sistema == sistema).first()
    if not config:
        config = get_default_config(sistema)
        db.add(config)
        db.commit()
        db.refresh(config)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(config, field, value)

    db.commit()
    db.refresh(config)
    return config


# ==========================================
# ENDPOINTS CATÁLOGO / ITEMS DE TIENDA
# ==========================================
@router.get("/items", response_model=List[TiendaItemResponse])
def get_tienda_items(
    sistema: str = Query(..., description="Sistema ('conlineweb' o 'hostingpro')"),
    solo_activos: bool = Query(False, description="Filtrar solo items activos"),
    db: Session = Depends(get_db)
):
    """Obtiene los paquetes/servicios disponibles en el catálogo de la tienda."""
    query = db.query(TiendaItem).filter(TiendaItem.sistema == sistema)
    if solo_activos:
        query = query.filter(TiendaItem.activo == 1)
    return query.order_by(asc(TiendaItem.orden), asc(TiendaItem.id)).all()


@router.post("/items", response_model=TiendaItemResponse, status_code=status.HTTP_201_CREATED)
def create_tienda_item(
    payload: TiendaItemCreate,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Crea un nuevo paquete o servicio en el catálogo de la tienda."""
    ensure_admin(current_user)
    item = TiendaItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/items/{item_id}", response_model=TiendaItemResponse)
def update_tienda_item(
    item_id: int,
    payload: TiendaItemUpdate,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Actualiza un paquete o servicio del catálogo."""
    ensure_admin(current_user)
    item = db.query(TiendaItem).filter(TiendaItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item de tienda no encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}")
def delete_tienda_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Elimina un paquete o servicio del catálogo."""
    ensure_admin(current_user)
    item = db.query(TiendaItem).filter(TiendaItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item de tienda no encontrado")

    db.delete(item)
    db.commit()
    return {"message": "Item eliminado correctamente", "id": item_id}


# ==========================================
# ENDPOINTS PREGUNTAS FRECUENTES (FAQS)
# ==========================================
@router.get("/faqs", response_model=List[TiendaFaqResponse])
def get_tienda_faqs(
    sistema: str = Query(..., description="Sistema ('conlineweb' o 'hostingpro')"),
    solo_activos: bool = Query(False, description="Filtrar solo faqs activas"),
    db: Session = Depends(get_db)
):
    """Obtiene las preguntas frecuentes de la tienda."""
    query = db.query(TiendaFaq).filter(TiendaFaq.sistema == sistema)
    if solo_activos:
        query = query.filter(TiendaFaq.activo == 1)
    return query.order_by(asc(TiendaFaq.orden), asc(TiendaFaq.id)).all()


@router.post("/faqs", response_model=TiendaFaqResponse, status_code=status.HTTP_201_CREATED)
def create_tienda_faq(
    payload: TiendaFaqCreate,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Crea una nueva pregunta frecuente."""
    ensure_admin(current_user)
    faq = TiendaFaq(**payload.model_dump())
    db.add(faq)
    db.commit()
    db.refresh(faq)
    return faq


@router.put("/faqs/{faq_id}", response_model=TiendaFaqResponse)
def update_tienda_faq(
    faq_id: int,
    payload: TiendaFaqUpdate,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Actualiza una pregunta frecuente."""
    ensure_admin(current_user)
    faq = db.query(TiendaFaq).filter(TiendaFaq.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="Pregunta frecuente no encontrada")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(faq, field, value)

    db.commit()
    db.refresh(faq)
    return faq


@router.delete("/faqs/{faq_id}")
def delete_tienda_faq(
    faq_id: int,
    db: Session = Depends(get_db),
    current_user: UserProfile = Depends(get_current_user)
):
    """Elimina una pregunta frecuente."""
    ensure_admin(current_user)
    faq = db.query(TiendaFaq).filter(TiendaFaq.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="Pregunta frecuente no encontrada")

    db.delete(faq)
    db.commit()
    return {"message": "Pregunta frecuente eliminada correctamente", "id": faq_id}
