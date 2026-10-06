<div align="center">

# ⚡ Puvnex CRM — Backend API
### *High-Performance Cloud Enterprise API & Orchestration Engine*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT%20Bearer-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)

<br/>

*API REST asíncrona de alto rendimiento diseñada para la gestión integral de clientes, infraestructura cloud (dominios y hosting), facturación, soporte técnico y portal de autoservicio.*

---

</div>

## 📑 Tabla de Contenidos

- [✨ Características Principales](#-características-principales)
- [🏛️ Arquitectura & Stack Tecnológico](#️-arquitectura--stack-tecnológico)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [🔐 Control de Acceso por Roles (RBAC)](#-control-de-acceso-por-roles-rbac)
- [🚀 Inicio Rápido](#-inicio-rápido)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalación](#instalación)
  - [Variables de Entorno](#variables-de-entorno)
  - [Ejecución](#ejecución)
- [📡 Módulos de la API & Endpoints](#-módulos-de-la-api--endpoints)
- [📚 Documentación Interactiva](#-documentación-interactiva)

---

## ✨ Características Principales

- ⚡ **Asíncrono & Ultrarrápido**: Desarrollado sobre FastAPI y Uvicorn ASGI para máxima concurrencia.
- 🛡️ **Seguridad Corporativa**: Autenticación Bearer JWT con rotación controlada, compatibilidad Bcrypt y protección contra inyecciones SQL.
- 👥 **Sistema RBAC Granular**: Permisos diferenciados por rol (Super Admin, Agentes, Clientes, Ventas, etc.).
- 📊 **Métricas en Tiempo Real**: Endpoints de analíticas, KPIs financieros y estado de servicios.
- 🌐 **Soporte Multi-Database**: Mapeo relacional optimizado con pool de conexiones para bases de datos principales y auxiliares.
- 📧 **Servicio de Notificaciones**: Integración SMTP transaccional para alertas de cobro, tickets y bienvenidas.

---

## 🏛️ Arquitectura & Stack Tecnológico

```
┌──────────────────────────────────────────────────────────┐
│                   Cliente Web (Vite/Vue 3)               │
└────────────────────────────┬─────────────────────────────┘
                             │  HTTP / JSON (REST API)
                             ▼
┌──────────────────────────────────────────────────────────┐
│                  Uvicorn ASGI Server                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │               FastAPI Application Router           │  │
│  │   ┌──────────────┐ ┌──────────────┐ ┌───────────┐  │  │
│  │   │  Auth & RBAC │ │  Dashboard   │ │  CRM Core │  │  │
│  │   └──────┬───────┘ └──────┬───────┘ └─────┬─────┘  │  │
│  └──────────┼────────────────┼───────────────┼────────┘  │
│             ▼                ▼               ▼           │
│  ┌────────────────────────────────────────────────────┐  │
│  │         SQLAlchemy ORM + Pydantic v2 Models        │  │
│  └───────────────────────────┬────────────────────────┘  │
└──────────────────────────────┼───────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────┐
│             MariaDB / MySQL Relational Database          │
└──────────────────────────────────────────────────────────┘
```

| Capa | Tecnología | Propósito |
| :--- | :--- | :--- |
| **API Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Enrutamiento asíncrono, OpenAPI y serialización |
| **Servidor ASGI** | [Uvicorn](https://www.uvicorn.org/) | Servidor de producción de baja latencia |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Modelado relacional y transacciones atómicas |
| **Base de Datos** | [PyMySQL](https://pymysql.readthedocs.io/) | Driver de conexión a MariaDB / MySQL |
| **Validación** | [Pydantic v2](https://docs.pydantic.dev/) | Tipado estricto, esquemas DTO y settings |
| **Criptografía** | [PyJWT](https://pyjwt.readthedocs.io/) + [Bcrypt](https://pypi.org/project/bcrypt/) | Autenticación JWT y hashing de contraseñas |

---

## 📂 Estructura del Proyecto

```bash
Puvnex_backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/        # Controladores por dominio (Auth, Clientes, Pagos, etc.)
│   │       └── api.py            # Enrutador centralizado API v1
│   ├── core/
│   │   ├── config.py             # Configuración y variables de entorno tipadas
│   │   ├── database.py           # Engine de BD, sesiones y dependencias
│   │   └── security.py           # Generación de tokens JWT y hashing seguro
│   ├── models/                   # Modelos relacionales ORM (SQLAlchemy)
│   ├── schemas/                  # Esquemas DTO de validación (Pydantic v2)
│   ├── services/                 # Servicios de negocio (Email, Webhooks, etc.)
│   └── main.py                   # Fábrica de aplicación FastAPI & Middlewares CORS
├── .env.example                  # Plantilla de variables de entorno
├── .gitignore                    # Reglas de exclusión de Git
├── requirements.txt              # Dependencias del proyecto
├── run.py                        # Script de arranque del servidor
└── README.md                     # Documentación oficial
```

---

## 🔐 Control de Acceso por Roles (RBAC)

| Nivel de Rol | Identificador | Descripción |
| :---: | :--- | :--- |
| `0` | **Cliente** | Acceso restringido a sus propios servicios y tickets |
| `1` | **Super Administrador** | Acceso total a configuración, finanzas y auditoría |
| `2` | **Operaciones / Solicitudes** | Gestión técnica de hosting, dominios y requerimientos |
| `3` | **Agente / Desarrollador** | Atención a tickets y proyectos técnicos |
| `4` | **Empresa / Partner** | Gestión de cuentas corporativas |
| `5` | **Ventas & Leads** | Seguimiento comercial y prospección |

---

## 🚀 Inicio Rápido

### Requisitos Previos

- **Python 3.11+**
- **MariaDB** o **MySQL 8.0+**
- **Git**

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone git@github.com:Paulob0t/Puvnex_backend.git
   cd Puvnex_backend
   ```

2. **Crear y activar el entorno virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Variables de Entorno

Copia el archivo de ejemplo y edita tus credenciales:

```bash
cp .env.example .env
```

```ini
# Configuración Principal
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=tu_clave_secreta_aqui

# Seguridad JWT
JWT_SECRET_KEY=tu_jwt_secret_key_super_segura
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Base de Datos MariaDB / MySQL
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASS=tu_password
DB_NAME=admin_clientes

# Servidor ASGI
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### Ejecución

```bash
# Opción 1: Mediante el ejecutor directo
python run.py

# Opción 2: Mediante Uvicorn CLI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📡 Módulos de la API & Endpoints

Todos los endpoints están prefijados bajo `/api/v1`:

| Módulo | Prefijo | Descripción |
| :--- | :--- | :--- |
| **Auth** | `/auth` | Inicio de sesión, validación de sesión y refresh tokens |
| **Clientes** | `/clientes` | CRUD completo, búsqueda avanzada y métricas de clientes |
| **Dominios** | `/dominios` | Administración de dominios, DNS y recordatorios de vencimiento |
| **Hostings** | `/hostings` | Gestión de planes, servidores y configuraciones técnicas |
| **Pagos** | `/pagos` | Registro financiero, cobros, balances y conciliación |
| **Portal** | `/portal` | Endpoints optimizados para el autoservicio de clientes |
| **Recordatorios**| `/recordatorios`| Gestión y envío automatizado de alertas |
| **Solicitudes** | `/solicitudes` | Sistema de tickets, soporte técnico y notas internas |
| **Dashboard** | `/dashboard` | KPIs ejecutivos, gráficos financieros y distribución |

---

## 📚 Documentación Interactiva

Con el servidor en ejecución, puedes explorar y probar la API en tiempo real:

- 📑 **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📖 **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- 🩺 **Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

<div align="center">

Desarrollado con ❤️ por **Paulo Essau** • *Puvnex Suite Cloud*

</div>
