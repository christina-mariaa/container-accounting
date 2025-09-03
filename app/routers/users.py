from fastapi import APIRouter, Depends, status

from app.schemas import SUserCreate, SUserLogin, SAuthTokensPair, SAuthAccessToken
from app.db import SessionDep
from app.repositories.users import UserRepository
from app.services.users import UserService
from app.auth import auth


router = APIRouter(
    prefix="/api/auth",
    tags=["Пользователи"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: SUserCreate, session: SessionDep):
    repo = UserRepository(session)
    service = UserService(repo)

    await service.register_user(user)
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(credentials: SUserLogin, session: SessionDep) -> SAuthTokensPair:
    repo = UserRepository(session)
    service = UserService(repo)

    access, refresh = await service.login_user(credentials)
    return SAuthTokensPair(access_token=access, refresh_token=refresh)


@router.post("/refresh-token")
async def refresh(token=Depends(auth.refresh_token_required)) -> SAuthAccessToken:
    new_access = auth.create_access_token(uid=token.subject)
    return SAuthAccessToken(access_token=new_access)
