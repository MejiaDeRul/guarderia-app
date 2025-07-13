from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.views import user_view
from app.database.session import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar
    create_tables()
    yield
    # Código que se ejecuta al cerrar (opcional)
    # por ejemplo: cerrar conexiones, limpiar recursos, etc.

app = FastAPI(title="FastAPI MVC App", lifespan=lifespan)

# Rutas
app.include_router(user_view.router)
