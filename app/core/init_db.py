import logging
from app.core.database import engine, Base, SessionLocal
import app.models  # Importa todos los modelos para que Base.metadata los reconozca
from app.models.login import Login
from app.models.cliente import Cliente
from app.core.security import hash_password

logger = logging.getLogger("puvnex.init_db")


def init_db():
    """Inicializa las tablas en la base de datos y crea usuarios por defecto si no existen."""
    try:
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos verificadas/creadas exitosamente.")

        # Verificar y sembrar usuarios por defecto
        db = SessionLocal()
        try:
            # 1. Super Administrador (Rol 1)
            admin = db.query(Login).filter(Login.usuario == "admin").first()
            if not admin:
                nuevo_admin = Login(
                    usuario="admin",
                    contrasena=hash_password("admin123"),
                    contrasena_normal="admin123",
                    id_tipo_usuario=1,  # 1 = Super Administrador
                    cambio_contrasena=0
                )
                db.add(nuevo_admin)
                db.commit()
                logger.info("Usuario administrador creado: admin / admin123 (Rol 1)")
            else:
                logger.info("Usuario administrador 'admin' ya existente.")

            # 2. Cliente de Prueba (Rol 0)
            cliente_user = db.query(Login).filter(Login.usuario == "cliente").first()
            if not cliente_user:
                # Buscar primer cliente registrado o crear uno
                cli_db = db.query(Cliente).first()
                cli_id = cli_db.id if cli_db else 2

                nuevo_cliente = Login(
                    id=cli_id,
                    usuario="cliente",
                    contrasena=hash_password("cliente123"),
                    contrasena_normal="cliente123",
                    id_tipo_usuario=0,  # 0 = Cliente
                    cambio_contrasena=0
                )
                db.add(nuevo_cliente)
                db.commit()
                logger.info(f"Usuario cliente creado: cliente / cliente123 (Rol 0, Cliente ID #{cli_id})")
            else:
                logger.info("Usuario cliente 'cliente' ya existente.")

            # 3. Sembrar Configuración y Catálogo Inicial de Tiendas (Puvnext Web y Puvnext Bot)
            from app.models.tienda import TiendaConfig, TiendaItem, TiendaFaq

            # 3.1 Tienda Puvnext Web (conlineweb)
            config_web = db.query(TiendaConfig).filter(TiendaConfig.sistema == "conlineweb").first()
            if not config_web:
                db.add(TiendaConfig(
                    sistema="conlineweb",
                    hero_badge="Soluciones Digitales & Desarrollo Web",
                    hero_titulo="Diseño Web Profesional y Tiendas Online de Alto Impacto",
                    hero_subtitulo="Desarrollamos la presencia en línea de tu empresa con diseño exclusivo, velocidad ultrarrápida, SEO integrado y soporte continuo.",
                    hero_cta_texto="Explorar Paquetes Web",
                    hero_cta_enlace="#catalogo",
                    whatsapp_contacto="5215500000000",
                    whatsapp_mensaje="Hola, me gustaría cotizar un desarrollo web para mi empresa en Puvnext Web.",
                    email_contacto="ventas@puvnex.io",
                    anuncio_activo=1,
                    anuncio_texto="🚀 ¡Lanza tu sitio web este mes con dominio y hosting incluido!",
                ))
                db.commit()

            # Items iniciales Web
            if db.query(TiendaItem).filter(TiendaItem.sistema == "conlineweb").count() == 0:
                items_web = [
                    TiendaItem(
                        sistema="conlineweb",
                        nombre="Landing Page Express",
                        categoria="Diseño Web",
                        descripcion="Página de aterrizaje optimizada para conversión y captura de leads.",
                        precio=3500.0,
                        periodo="pago único",
                        moneda="MXN",
                        caracteristicas="Diseño One-Page responsivo\nFormulario de contacto a WhatsApp\nOptimización de carga ultra rápida\nDominio .com gratis por 1 año\nCertificado SSL incluido",
                        destacado=0,
                        activo=1,
                        orden=1
                    ),
                    TiendaItem(
                        sistema="conlineweb",
                        nombre="Sitio Web Corporativo Pro",
                        categoria="Desarrollo Web",
                        descripcion="Sitio web completo de hasta 5 secciones para empresas y marcas líderes.",
                        precio=6800.0,
                        periodo="pago único",
                        moneda="MXN",
                        caracteristicas="Hasta 5 secciones personalizadas\nPanel autoadministrable intuitivo\nIntegración SEO Google inicial\nCorreos corporativos configurados\n1 Año de Hosting de alta velocidad\nSoporte prioritario 30 días",
                        destacado=1,
                        activo=1,
                        orden=2
                    ),
                    TiendaItem(
                        sistema="conlineweb",
                        nombre="E-commerce / Tienda Online",
                        categoria="Comercio Electrónico",
                        descripcion="Plataforma de ventas online con pasarela de pagos y catálogo ilimitado.",
                        precio=12500.0,
                        periodo="pago único",
                        moneda="MXN",
                        caracteristicas="Catálogo de productos ilimitado\nPasarelas Stripe, MercadoPago, PayPal\nGestión de stock e inventario\nNotificaciones automáticas por WhatsApp\nCapacitación y soporte incluido",
                        destacado=0,
                        activo=1,
                        orden=3
                    ),
                ]
                db.add_all(items_web)
                db.commit()

            # 3.2 Tienda Puvnext Bot (hostingpro)
            config_bot = db.query(TiendaConfig).filter(TiendaConfig.sistema == "hostingpro").first()
            if not config_bot:
                db.add(TiendaConfig(
                    sistema="hostingpro",
                    hero_badge="Infraestructura Cloud & Servidores 2026",
                    hero_titulo="Servidores de Alto Rendimiento y Bots Inteligentes",
                    hero_subtitulo="Alojamiento web ultra rápido con almacenamiento NVMe, copias de seguridad automáticas, soporte 24/7 y automatizaciones para tu negocio.",
                    hero_cta_texto="Ver Planes de Hosting",
                    hero_cta_enlace="#catalogo",
                    whatsapp_contacto="5215500000000",
                    whatsapp_mensaje="Hola, me gustaría cotizar un servidor o plan de hosting en Puvnext Bot.",
                    email_contacto="contacto@puvnex.io",
                    anuncio_activo=1,
                    anuncio_texto="🔥 20% de descuento en la contratación anual de cualquier plan Cloud.",
                ))
                db.commit()

            # Items iniciales Bot / Hosting
            if db.query(TiendaItem).filter(TiendaItem.sistema == "hostingpro").count() == 0:
                items_bot = [
                    TiendaItem(
                        sistema="hostingpro",
                        nombre="Cloud Hosting Starter",
                        categoria="Hosting Compartido",
                        descripcion="Ideal para sitios web personales, blogs o pequeños emprendimientos.",
                        precio=149.0,
                        periodo="/mes",
                        moneda="MXN",
                        caracteristicas="10 GB Almacenamiento NVMe\nTráfico mensual no medido\n5 Cuentas de correo profesional\nCertificados SSL ilimitados\nPanel de control cPanel/Plesk\nRespaldos semanales",
                        destacado=0,
                        activo=1,
                        orden=1
                    ),
                    TiendaItem(
                        sistema="hostingpro",
                        nombre="Cloud Hosting Business Pro",
                        categoria="Hosting Empresarial",
                        descripcion="Máxima velocidad para sitios de alto tráfico y tiendas en línea.",
                        precio=349.0,
                        periodo="/mes",
                        moneda="MXN",
                        caracteristicas="50 GB Almacenamiento NVMe puro\nRecursos dedicados de CPU y RAM\nCorreos corporativos ilimitados\nDominio .com gratis por 1 año\nRespaldos diarios automáticos\nSoporte técnico 24/7 prioritario",
                        destacado=1,
                        activo=1,
                        orden=2
                    ),
                    TiendaItem(
                        sistema="hostingpro",
                        nombre="VPS Cloud Server Dedicado",
                        categoria="Servidores VPS",
                        descripcion="Control total y potencia dedicada para sistemas y aplicaciones críticas.",
                        precio=899.0,
                        periodo="/mes",
                        moneda="MXN",
                        caracteristicas="4 vCPU Cores & 8 GB RAM\n120 GB Almacenamiento NVMe RAID 10\nIP Dedicada incluida\nAcceso Root completo\nMonitorización y uptime 99.9%\nProtección Anti-DDoS avanzada",
                        destacado=0,
                        activo=1,
                        orden=3
                    ),
                ]
                db.add_all(items_bot)
                db.commit()

        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        raise e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
