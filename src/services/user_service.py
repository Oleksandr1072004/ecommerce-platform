"""User business logic: registration, authentication, profile updates."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from src.models.user import User, UserRole
from src.schemas.user import Token, UserCreate, UserRegister


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db

    # ---------- Queries ----------

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    # ---------- Registration ----------

    def register(self, payload: UserRegister) -> User:
        if self.get_by_email(payload.email):
            raise ValueError("Email already registered")

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            role=UserRole.CUSTOMER,  # force — never trust the client
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_admin(self, payload: UserCreate) -> User:
        """Internal / seed helper — bypasses public registration."""
        if self.get_by_email(payload.email):
            raise ValueError("Email already registered")

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
            role=UserRole.ADMIN,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ---------- Login ----------

    def authenticate(self, email: str, password: str) -> Token | None:
        user = self.get_by_email(email)
        if user is None or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return Token(
            access_token=create_access_token(str(user.id), user.role.value),
            refresh_token=create_refresh_token(str(user.id)),
        )

    # ---------- Profile ----------

    def update_profile(self, user: User, full_name: str | None) -> User:
        if full_name is not None:
            user.full_name = full_name
        self.db.commit()
        self.db.refresh(user)
        return user