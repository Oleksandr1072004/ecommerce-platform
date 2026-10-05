import pytest
import fakeredis
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.database import Base, get_db
from src.main import app
from src.models.user import User, UserRole  # noqa: F401 — ensure models are registered
from src.services.user_service import UserService
from src.schemas.user import UserCreate, UserRegister
from src.core import redis_client as rc

rc.redis_client = fakeredis.FakeRedis(decode_responses=True)

# In-memory SQLite, shared across connections
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(autouse=True)
def _setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def customer(db):
    return UserService(db).register(
        UserRegister(email="customer@test.com", password="customer123", full_name="Cust")
    )


@pytest.fixture
def admin(db):
    return UserService(db).create_admin(
        UserCreate(email="admin@test.com", password="admin12345", full_name="Admin")
    )


@pytest.fixture
def customer_token(client, customer):
    r = client.post("/api/v1/auth/login", json={"email": "customer@test.com", "password": "customer123"})
    return r.json()["access_token"]


@pytest.fixture
def admin_token(client, admin):
    r = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "admin12345"})
    return r.json()["access_token"]