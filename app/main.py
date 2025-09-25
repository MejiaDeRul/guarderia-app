from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session


from app.config import settings
from app.database.session import engine, SessionLocal
from app.models.base import Base


from app.views import auth as auth_router
from app.views import users as users_router
from app.views import class_groups as class_groups_router
from app.views import children as children_router
from app.views import enrollments as enrollments_router
from app.views import events as events_router
from app.views import messages as messages_router


app = FastAPI(title="Guarderia API")


# CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables (for dev only; use Alembic in prod)
Base.metadata.create_all(bind=engine)


# Routers
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(class_groups_router.router)
app.include_router(children_router.router)
app.include_router(enrollments_router.router)
app.include_router(events_router.router)
app.include_router(messages_router.router)


@app.get("/health")
def health():
    with SessionLocal() as db:
        db.execute(text("SELECT 1"))
    return {"status": "ok"}