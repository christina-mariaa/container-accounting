from app.repositories.containers import ContainersRepository
from app.models import Container
from app.schemas import SContainerCreate
from decimal import Decimal
from fastapi import HTTPException, status


class ContainersService:
    def __init__(self, repo: ContainersRepository):
        self.repo = repo

    async def list_or_search(self, q: str | None):
        if q:
            return await self.repo.search_by_number(q.strip().upper())
        return await self.repo.list_first(50)

    async def by_cost(self, cost: Decimal | None, min_cost: Decimal | None, max_cost: Decimal | None):
        if cost is not None and (min_cost is not None or max_cost is not None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Use either 'cost' or 'min/max', not both")

        def ensure_two_dec(v: Decimal, name: str):
            if v.as_tuple().exponent < -2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"{name} must have at most two decimal places")

        if cost is not None:
            ensure_two_dec(cost, "cost")
            if cost <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="cost must be positive")
            return await self.repo.search_by_cost_exact(cost)

        if min_cost is None and max_cost is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Provide either 'cost' or at least one of 'min'/'max'")

        if min_cost is not None:
            ensure_two_dec(min_cost, "min")
            if min_cost <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="min must be positive")
        if max_cost is not None:
            ensure_two_dec(max_cost, "max")
            if max_cost <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="max must be positive")

        return await self.repo.search_by_cost_range(min_cost, max_cost)

    async def create(self, data: SContainerCreate) -> Container:
        return await self.repo.create(data)
