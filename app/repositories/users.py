from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import User
from app.schemas import SUserCreate
from app.security import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_name(self, user_name: str) -> User | None:
        query = select(User).where(User.username == user_name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(self, data: SUserCreate) -> User:
        user_dict = data.model_dump()
        user_dict["password"] = hash_password(user_dict["password"])

        user = User(**user_dict)

        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")

        await self.session.refresh(user)
        return user
