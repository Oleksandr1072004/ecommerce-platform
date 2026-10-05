from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.user import User, UserRole
from src.schemas.user import LoginRequest, Token, UserOut, UserRegister, UserUpdate
from src.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> UserOut:
    try:
        user = UserService(db).register(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return UserOut.model_validate(user)


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> Token:
    token = UserService(db).authenticate(payload.email, payload.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Set HttpOnly cookie so browser pages (e.g. /dashboard) work
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        secure=False,   # set True in production
        max_age=settings.access_token_expire_minutes * 60,
    )
    return token


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"detail": "Logged out"}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)


@router.patch("/me", response_model=UserOut)
def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserOut:
    user = UserService(db).update_profile(current_user, payload.full_name)
    return UserOut.model_validate(user)

@router.patch("/users/{user_id}/profile", response_model=UserOut)
def update_user_profile(
    user_id: int,
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserOut:
    """A user can only update their own profile — unless they're an admin."""
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Cannot modify another user's profile")

    target = UserService(db).get_by_id(user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated = UserService(db).update_profile(target, payload.full_name)
    return UserOut.model_validate(updated)


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    return {"detail": "Logged out"}