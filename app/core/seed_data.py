import logging
from datetime import date, datetime, timedelta, time
from sqlalchemy import text
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
import app.models  # Asegura todos los modelos
from app.models.login import Login
from app.models.cliente import Cliente
from app.models.dominio import Dominio
from app.models.hosting import Hosting
from app.models.pago import Pago
from app.models.solicitud import Solicitud

logger = logging.getLogger("puvnex.seed")


def ensure_client_logins():
    """Garantiza que todos los clientes en la base de datos tengan sus credenciales en la tabla login y su login_id vinculado."""
    db = SessionLocal()
    try:
        # Sincronizar secuencia de login primero
        db.execute(text("SELECT setval('login_id_seq', COALESCE((SELECT MAX(id) FROM login), 1));"))
        db.commit()

        clientes = db.query(Cliente).filter(Cliente.eliminado == 0).all()
        created_count = 0
        linked_count = 0
        for c in clientes:
            if not c.correo:
                continue
            email_clean = c.correo.strip().lower()
            login_record = db.query(Login).filter(Login.usuario == email_clean).first()
            if not login_record:
                plain_pass = f"Puvnex{c.id}*"
                hashed = hash_password(plain_pass)
                login_record = Login(
                    usuario=email_clean,
                    contrasena=hashed,
                    contrasena_normal=plain_pass,
                    id_tipo_usuario=0,  # 0 = Cliente
                    cambio_contrasena=0,
                )
                db.add(login_record)
                db.flush()
                created_count += 1
                logger.info(f"Creado acceso login para cliente '{c.empresa}': usuario={email_clean}, pass={plain_pass}")
            
            if c.login_id != login_record.id:
                c.login_id = login_record.id
                linked_count += 1

        db.commit()
        logger.info(f"✓ Acceso a login sincronizado ({created_count} creados, {linked_count} vinculados).")
    except Exception as e:
        db.rollback()
        logger.error(f"Error sincronizando accesos de login: {e}")
        raise e
    finally:
        db.close()


def seed_test_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    hoy = date.today()
    
    try:
        # Verificar si ya existen clientes para no duplicar
        count = db.query(Cliente).count()
        if count > 0:
            logger.info(f"Ya existen {count} clientes en la base de datos. Sincronizando usuarios...")
            ensure_client_logins()
            return

        logger.info("Iniciando sembrado de clientes de prueba para ConlineWeb y HostingPro...")

        # -------------------------------------------------------------
        # 1. CLIENTES CONLINEWEB
        # -------------------------------------------------------------
        c1 = Cliente(
            nombre_contacto="Carlos Mendoza",
            empresa="TechNova Solutions S.A. de C.V.",
            correo="carlos@technova.mx",
            telefono="5214771234567",
            rsocial="TechNova Solutions S.A. de C.V.",
            rfc="TNO190412AB1",
            calle="Av. Insurgentes Sur",
            next="1450",
            col="Crédito Constructor",
            cp="03940",
            pais="México",
            estado="CDMX",
            ciudad="Ciudad de México",
            display="conlineweb",
            eliminado=0,
            transferido=0
        )
        db.add(c1)
        db.flush()

        d1 = Dominio(
            cliente_id=c1.id,
            url_dominio="technova.mx",
            fecha_contratacion=hoy - timedelta(days=200),
            fecha_pago=hoy + timedelta(days=45),
            costo_dominio=450.0,
            estado_dominio=1,
            eliminado=0
        )
        db.add(d1)
        db.flush()

        h1 = Hosting(
            cliente_id=c1.id,
            nom_host="cPanel Cloud Enterprise",
            dominio="technova.mx",
            usuario="technova",
            costo_producto=1450.0,
            fecha_contratacion=hoy - timedelta(days=200),
            fecha_pago=hoy + timedelta(days=15),
            estado_producto=1,
            eliminado=0
        )
        db.add(h1)
        db.flush()

        # Pagos c1 (uno pagado, uno pendiente)
        p1_1 = Pago(
            id_clie=c1.id,
            tipo_servicio=1,
            id_servicio=h1.id_orden,
            fecha=hoy - timedelta(days=30),
            hora=time(10, 30),
            fecha_pago=hoy - timedelta(days=28),
            hora_pago=time(11, 0),
            monto=1450.0,
            currency="MXN",
            concepto="Renovación Hosting Cloud Enterprise - Mes Anterior",
            estatus=1,  # Pagado
            sistema="conlineweb"
        )
        p1_2 = Pago(
            id_clie=c1.id,
            tipo_servicio=1,
            id_servicio=h1.id_orden,
            fecha=hoy,
            hora=time(9, 0),
            fecha_limite_pago=hoy + timedelta(days=15),
            monto=1450.0,
            currency="MXN",
            concepto="Renovación Hosting Cloud Enterprise - Mes Actual",
            estatus=0,  # Pendiente
            sistema="conlineweb"
        )
        db.add_all([p1_1, p1_2])

        # Cliente 2: Prisma Inmobiliaria
        c2 = Cliente(
            nombre_contacto="Valeria Robles",
            empresa="Grupo Inmobiliario Prisma",
            correo="vrobles@prismainmo.com",
            telefono="5214779876543",
            rsocial="Grupo Inmobiliario Prisma S.A.P.I.",
            rfc="GIP210805XY9",
            calle="Blvd. Campestre",
            next="204",
            col="Jardines del Moral",
            cp="37160",
            pais="México",
            estado="Guanajuato",
            ciudad="León",
            display="conlineweb",
            eliminado=0,
            transferido=0
        )
        db.add(c2)
        db.flush()

        d2 = Dominio(
            cliente_id=c2.id,
            url_dominio="prismainmo.com",
            fecha_contratacion=hoy - timedelta(days=380),
            fecha_pago=hoy - timedelta(days=3),
            costo_dominio=390.0,
            estado_dominio=1,
            eliminado=0
        )
        h2 = Hosting(
            cliente_id=c2.id,
            nom_host="Hosting WordPress Pro",
            dominio="prismainmo.com",
            usuario="prismainmo",
            costo_producto=850.0,
            fecha_contratacion=hoy - timedelta(days=380),
            fecha_pago=hoy - timedelta(days=3),
            estado_producto=1,
            eliminado=0
        )
        db.add_all([d2, h2])
        db.flush()

        # Pago vencido c2
        p2_1 = Pago(
            id_clie=c2.id,
            tipo_servicio=1,
            id_servicio=h2.id_orden,
            fecha=hoy - timedelta(days=10),
            hora=time(14, 0),
            fecha_limite_pago=hoy - timedelta(days=3),
            monto=850.0,
            currency="MXN",
            concepto="Renovación Anual Hosting WordPress Pro (Vencido)",
            estatus=0,  # Pendiente
            sistema="conlineweb"
        )
        db.add(p2_1)

        # Cliente 3: Logística Alianza
        c3 = Cliente(
            nombre_contacto="Roberto Garza",
            empresa="Logística y Transporte Alianza",
            correo="contacto@alianzalog.com",
            telefono="5218115551234",
            rsocial="Alianza Transportes de Carga S.A.",
            rfc="LTA180220KL3",
            ciudad="Monterrey",
            estado="Nuevo León",
            pais="México",
            display="conlineweb",
            eliminado=0,
            transferido=0
        )
        db.add(c3)
        db.flush()

        h3 = Hosting(
            cliente_id=c3.id,
            nom_host="Servidor VPS NVMe 4GB",
            dominio="alianzalog.com",
            usuario="alianzavps",
            costo_producto=2200.0,
            fecha_contratacion=hoy - timedelta(days=90),
            fecha_pago=hoy + timedelta(days=20),
            estado_producto=1,
            eliminado=0
        )
        db.add(h3)
        db.flush()

        p3_1 = Pago(
            id_clie=c3.id,
            tipo_servicio=1,
            id_servicio=h3.id_orden,
            fecha=hoy - timedelta(days=5),
            hora=time(16, 20),
            fecha_pago=hoy - timedelta(days=2),
            hora_pago=time(17, 0),
            monto=2200.0,
            currency="MXN",
            concepto="Pago Mensual Servidor VPS NVMe",
            estatus=1,  # Pagado este mes
            sistema="conlineweb"
        )
        db.add(p3_1)

        # -------------------------------------------------------------
        # 2. CLIENTES HOSTINGPRO
        # -------------------------------------------------------------
        c4 = Cliente(
            nombre_contacto="Mauricio Estrada",
            empresa="Nexus Digital Marketing Agency",
            correo="mau@nexusdigital.agency",
            telefono="5215541112233",
            rsocial="Nexus Digital Media S.A. de C.V.",
            rfc="NDM220115M10",
            calle="Paseo de la Reforma",
            next="505",
            col="Cuauhtémoc",
            cp="06500",
            ciudad="Ciudad de México",
            estado="CDMX",
            pais="México",
            display="hostingpro",
            eliminado=0,
            transferido=0
        )
        db.add(c4)
        db.flush()

        d4 = Dominio(
            cliente_id=c4.id,
            url_dominio="nexusdigital.agency",
            fecha_contratacion=hoy - timedelta(days=300),
            fecha_pago=hoy + timedelta(days=60),
            costo_dominio=650.0,
            estado_dominio=1,
            eliminado=0
        )
        h4 = Hosting(
            cliente_id=c4.id,
            nom_host="Hosting Reseller Ultra 50 cPanel",
            dominio="nexusdigital.agency",
            usuario="nexusresell",
            costo_producto=3500.0,
            fecha_contratacion=hoy - timedelta(days=300),
            fecha_pago=hoy + timedelta(days=5),
            estado_producto=1,
            eliminado=0
        )
        db.add_all([d4, h4])
        db.flush()

        p4_1 = Pago(
            id_clie=c4.id,
            tipo_servicio=1,
            id_servicio=h4.id_orden,
            fecha=hoy,
            hora=time(11, 0),
            fecha_limite_pago=hoy + timedelta(days=5),
            monto=3500.0,
            currency="MXN",
            concepto="Plan Hosting Reseller Ultra 50 Cuentas",
            estatus=0,  # Pendiente próximo (5 días)
            sistema="hostingpro"
        )
        p4_2 = Pago(
            id_clie=c4.id,
            tipo_servicio=1,
            id_servicio=h4.id_orden,
            fecha=hoy - timedelta(days=30),
            hora=time(10, 0),
            fecha_pago=hoy - timedelta(days=29),
            hora_pago=time(12, 0),
            monto=3500.0,
            currency="MXN",
            concepto="Plan Hosting Reseller Ultra - Mes Pasado",
            estatus=1,  # Pagado
            sistema="hostingpro"
        )
        db.add_all([p4_1, p4_2])

        # Cliente 5: Apex Financial
        c5 = Cliente(
            nombre_contacto="Sofía Villarreal",
            empresa="Finanzas & Software Apex",
            correo="sofia@apexfin.co",
            telefono="5214429998877",
            rsocial="Apex Financial Technologies S.A.",
            rfc="AFT200910ZZ2",
            ciudad="Querétaro",
            estado="Querétaro",
            pais="México",
            display="hostingpro",
            eliminado=0,
            transferido=0
        )
        db.add(c5)
        db.flush()

        h5 = Hosting(
            cliente_id=c5.id,
            nom_host="Dedicated Server AMD EPYC 16-Core",
            dominio="apexfin.co",
            usuario="apexdedic",
            costo_producto=4800.0,
            fecha_contratacion=hoy - timedelta(days=120),
            fecha_pago=hoy - timedelta(days=4),
            estado_producto=1,
            eliminado=0
        )
        db.add(h5)
        db.flush()

        p5_1 = Pago(
            id_clie=c5.id,
            tipo_servicio=1,
            id_servicio=h5.id_orden,
            fecha=hoy - timedelta(days=12),
            hora=time(12, 0),
            fecha_limite_pago=hoy - timedelta(days=4),
            monto=4800.0,
            currency="MXN",
            concepto="Servidor Dedicado AMD EPYC (Vencido)",
            estatus=0,  # Pendiente Vencido
            sistema="hostingpro"
        )
        db.add(p5_1)

        # Cliente 6: E-Commerce Boutique
        c6 = Cliente(
            nombre_contacto="Diego Palacios",
            empresa="Boutique & E-Commerce Aurora",
            correo="diego@aurorashop.mx",
            telefono="5215567778899",
            rsocial="Boutique Aurora México S.A.",
            rfc="BAM230301TT8",
            ciudad="Guadalajara",
            estado="Jalisco",
            pais="México",
            display="hostingpro",
            eliminado=0,
            transferido=0
        )
        db.add(c6)
        db.flush()

        h6 = Hosting(
            cliente_id=c6.id,
            nom_host="Cloud E-Commerce Magento/Woo",
            dominio="aurorashop.mx",
            usuario="aurorashop",
            costo_producto=1800.0,
            fecha_contratacion=hoy - timedelta(days=60),
            fecha_pago=hoy + timedelta(days=25),
            estado_producto=1,
            eliminado=0
        )
        db.add(h6)
        db.flush()

        p6_1 = Pago(
            id_clie=c6.id,
            tipo_servicio=1,
            id_servicio=h6.id_orden,
            fecha=hoy - timedelta(days=4),
            hora=time(15, 0),
            fecha_pago=hoy - timedelta(days=3),
            hora_pago=time(15, 30),
            monto=1800.0,
            currency="MXN",
            concepto="Hosting Cloud E-Commerce Alta Concurrencia",
            estatus=1,  # Pagado este mes
            sistema="hostingpro"
        )
        db.add(p6_1)

        # Solicitudes de prueba
        sol1 = Solicitud(
            id_cliente=c1.id,
            titulo="Actualización de Certificados SSL y optimización PHP 8.3",
            descripcion="El cliente solicita validar la renovación automática de SSL Let's Encrypt y habilitar HTTP/2 en su cPanel.",
            prioridad="Alta",
            estado="En Proceso",
            fecha_solicitud=datetime.utcnow() - timedelta(days=1),
            fecha_lim=datetime.utcnow() + timedelta(days=2),
            usuario_asignado="admin"
        )
        sol2 = Solicitud(
            id_cliente=c4.id,
            titulo="Configuración de Zona DNS para CDN Cloudflare",
            descripcion="Migración de registros A, CNAME y MX hacia nameservers de Cloudflare para mitigar tráfico malicioso.",
            prioridad="Media",
            estado="Pendiente",
            fecha_solicitud=datetime.utcnow(),
            fecha_lim=datetime.utcnow() + timedelta(days=4),
            usuario_asignado="admin"
        )
        db.add_all([sol1, sol2])

        db.commit()
        logger.info("✓ 6 Clientes con servicios, dominios, hosting y pagos creados exitosamente.")
        
        # Sincronizar accesos login para todos los clientes creados
        ensure_client_logins()
    except Exception as e:
        db.rollback()
        logger.error(f"Error sembrando datos de prueba: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_test_data()
