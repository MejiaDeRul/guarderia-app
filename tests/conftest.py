import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.session import Base
from app.dependencies.db import get_db
from app.models import user as user_model  # asegura que las tablas se conozcan

# 🔧 Base de datos en memoria que persiste durante toda la sesión
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # <- esto mantiene la memoria viva
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas una sola vez
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
