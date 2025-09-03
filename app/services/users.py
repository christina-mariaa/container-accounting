from app.repositories.users import UserRepository
from app.models import User
from app.schemas import SUserLogin, SUserCreate
from app.security import verify_password
from app.auth import auth
from fastapi import HTTPException, status


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, user: SUserCreate) -> User:
        if await self.repo.get_by_name(user.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")

        return await self.repo.create_user(user)

    async def login_user(self, data: SUserLogin) -> tuple[str, str]:
        user = await self.repo.get_by_name(data.username)

        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access = auth.create_access_token(uid=str(user.id))
        refresh = auth.create_refresh_token(uid=str(user.id))

        return access, refresh
