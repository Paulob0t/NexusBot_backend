import logging
from app.core.database import engine, Base, SessionLocal
import app.models  # Importa todos los modelos para que Base.metadata los reconozca
from app.models.login import Login
from app.models.cliente import Cliente
from app.core.security import hash_password

logger = logging.getLogger("nexusbot.init_db")


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

        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        raise e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
