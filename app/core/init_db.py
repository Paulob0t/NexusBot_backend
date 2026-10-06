import logging
from app.core.database import engine, Base, SessionLocal
import app.models  # Importa todos los modelos para que Base.metadata los reconozca
from app.models.login import Login
from app.core.security import hash_password

logger = logging.getLogger("nexusbot.init_db")


def init_db():
    """Inicializa las tablas en la base de datos y crea el usuario admin por defecto si no existe."""
    try:
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos verificadas/creadas exitosamente.")

        # Verificar y sembrar usuario administrador
        db = SessionLocal()
        try:
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
                logger.info("Usuario administrador por defecto creado: admin / admin123")
            else:
                logger.info("Usuario administrador 'admin' ya existente.")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error inicializando base de datos: {e}")
        raise e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
