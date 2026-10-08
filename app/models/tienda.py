from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, SmallInteger
from app.core.database import Base


class TiendaConfig(Base):
    __tablename__ = "tienda_configs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sistema = Column(String(50), nullable=False, unique=True, index=True)  # 'conlineweb' | 'hostingpro'
    hero_badge = Column(String(100), nullable=True)
    hero_titulo = Column(String(200), nullable=False)
    hero_subtitulo = Column(Text, nullable=True)
    hero_cta_texto = Column(String(100), nullable=True)
    hero_cta_enlace = Column(String(255), nullable=True)
    whatsapp_contacto = Column(String(50), nullable=True)
    whatsapp_mensaje = Column(Text, nullable=True)
    email_contacto = Column(String(100), nullable=True)
    anuncio_activo = Column(SmallInteger, default=0, nullable=False)
    anuncio_texto = Column(String(255), nullable=True)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<TiendaConfig(sistema='{self.sistema}', titulo='{self.hero_titulo}')>"


class TiendaItem(Base):
    __tablename__ = "tienda_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sistema = Column(String(50), nullable=False, index=True)  # 'conlineweb' | 'hostingpro'
    nombre = Column(String(150), nullable=False)
    categoria = Column(String(100), nullable=True)  # 'Web', 'Landing', 'Hosting', 'Bots', etc.
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, default=0.0, nullable=False)
    periodo = Column(String(50), default="pago único", nullable=False)  # 'pago único', '/mes', '/año'
    moneda = Column(String(10), default="MXN", nullable=False)
    caracteristicas = Column(Text, nullable=True)  # Lista separada por saltos de línea (\n)
    destacado = Column(SmallInteger, default=0, nullable=False)  # 1 = Popular / Recomendado
    activo = Column(SmallInteger, default=1, nullable=False)  # 1 = Activo, 0 = Inactivo
    orden = Column(Integer, default=0, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<TiendaItem(id={self.id}, sistema='{self.sistema}', nombre='{self.nombre}', precio={self.precio})>"


class TiendaFaq(Base):
    __tablename__ = "tienda_faqs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sistema = Column(String(50), nullable=False, index=True)  # 'conlineweb' | 'hostingpro'
    pregunta = Column(String(255), nullable=False)
    respuesta = Column(Text, nullable=False)
    orden = Column(Integer, default=0, nullable=False)
    activo = Column(SmallInteger, default=1, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<TiendaFaq(id={self.id}, sistema='{self.sistema}', pregunta='{self.pregunta[:30]}...')>"
