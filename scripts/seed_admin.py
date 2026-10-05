from src.core.database import SessionLocal
from src.schemas.user import UserCreate
from src.services.user_service import UserService

with SessionLocal() as db:
    try:
        UserService(db).create_admin(
            UserCreate(email="admin@example.com", password="admin12345", full_name="Admin")
        )
        print("Admin created")
    except ValueError as e:
        print(f"Skipped: {e}")