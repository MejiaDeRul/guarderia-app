
---

## Estructura de carpetas (¿para qué sirve cada una?)

```
.
├─ app/
│ ├─ main.py # Punto de entrada FastAPI; registra middlewares y routers
│ ├─ config.py # Configuración (lee variables .env)
│ ├─ database/
│ │ └─ session.py # Conexión a Postgres (engine, SessionLocal, get_db)
│ ├─ models/ # Tablas/entidades SQLAlchemy (User, Child, ClassGroup, etc.)
│ ├─ schemas/ # Esquemas Pydantic (validación/serialización)
│ ├─ services/ # Lógica auxiliar (auth: hash/verificación y JWT)
│ ├─ dependencies/ # Dependencias reutilizables (RBAC: AdminOnly, etc.)
│ └─ views/ # Routers/Endpoints (auth, users, class-groups, children, enrollments, events, messages)
├─ requirements.txt # Dependencias Python
├─ Dockerfile # Imagen de la API (uvicorn)
├─ docker-compose.yml # Orquesta API + DB (PostgreSQL) con healthcheck
├─ .env.example # Variables de entorno de ejemplo (no subir .env real)
├─ .dockerignore # Archivos a excluir del build
└─ .gitignore # Ignora .env, .venv, cachés, etc.
```

---

## Variables de entorno
Copia .env.example a .env (en la raíz):

```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/guarderia
SECRET_KEY=change-me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```
La API usa el hostname db (el servicio de Postgres definido en Docker Compose).

---

## Cómo usar con Docker

1. Build & up
```bash
docker compose up -d --build
```
2. Ver logs
```bash
docker compose logs -f api
```
3. Probar
- Health: http://localhost:8000/health
- Swagger: http://localhost:8000/docs

Al primer arranque se crean las tablas (solo desarrollo). Para producción, usar Alembic.
---

## Flujo de prueba mínimo (en Swagger)

1. POST /auth/bootstrap-admin → crea el primer admin (una vez).
2. POST /auth/login → copia access_token y Authorize.
3. Usa /users, /class-groups, /children, /enrollments, /events, /messages según tu rol.

---

## Troubleshooting

- DB no lista: espera a que db esté healthy (docker compose ps, logs db).
- 401/403: revisa el token (Authorize) y el rol del usuario.
- Fechas: usar ISO 8601 (ej: 2025-10-01T13:00:00Z).

---

## 📄 Licencia

MIT © 2025 Juan Mejía
