# 🚀 NexusBot CRM - Backend (FastAPI)

API REST asíncrona de alto rendimiento para la Suite Cloud Empresarial NexusBot CRM.

---

## 🛠️ Stack Tecnológico

| Capa | Herramienta | Utilidad |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | API REST asíncrona de alto rendimiento con validación automática y OpenAPI. |
| **Servidor ASGI** | **Uvicorn** | Servidor web ASGI de producción / desarrollo. |
| **ORM / DB Driver** | **SQLAlchemy + PyMySQL** | Mapeo relacional de base de datos MariaDB/MySQL. |
| **Seguridad & Auth** | **PyJWT + Bcrypt / Passlib** | Autenticación basada en tokens JWT Bearer y hashing seguro de contraseñas. |
| **Configuración** | **Pydantic Settings** | Gestión tipada de variables de entorno mediante `.env`. |

---

## 🔒 Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura los accesos necesarios:

```bash
cp .env.example .env
```

Variables clave en `.env`:
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME`: Conexión MariaDB/MySQL.
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Configuración de tokens de autenticación.
- `BACKEND_HOST`, `BACKEND_PORT`: Host y puerto de escucha (default: `0.0.0.0:8000`).

---

## 💻 Instalación y Ejecución

### 1. Crear y activar el entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar en Linux/macOS
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Iniciar el servidor

```bash
# Opción 1: Vía script
python run.py

# Opción 2: Vía Uvicorn directo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📖 Documentación de la API

Una vez iniciado el backend, accede a la documentación interactiva:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)
