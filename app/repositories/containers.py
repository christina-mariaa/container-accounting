from decimal import Decimal
from typing import Sequence
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models import Container
from app.schemas import SContainerCreate


class ContainersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_first(self, limit: int = 50) -> Sequence[Container]:
        query = select(Container).order_by(Container.id.asc()).limit(limit)
        return (await self.session.execute(query)).scalars().all()

    async def search_by_number(self, q: str) -> Sequence[Container]:
        query = select(Container).where(Container.container_number.like(f"%{q}%")).order_by(Container.id.asc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_by_cost_exact(self, cost: Decimal) -> Sequence[Container]:
        query = select(Container).where(Container.cost == cost).order_by(Container.id.asc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def search_by_cost_range(self, min_cost: Decimal | None, max_cost: Decimal | None):
        clauses = []
        if min_cost is not None:
            clauses.append(Container.cost >= min_cost)
        if max_cost is not None:
            clauses.append(Container.cost <= max_cost)
        query = select(Container).where(and_(*clauses)).order_by(Container.id.asc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, data: SContainerCreate) -> Container:
        container = Container(**data.model_dump())
        self.session.add(container)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Container with this name already exists")
        await self.session.refresh(container)
        return container
