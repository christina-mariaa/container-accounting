from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionDep
from app.repositories.containers import ContainersRepository
from app.services.containers import ContainersService
from app.schemas import SContainerCreate, SContainerOut
from app.auth import get_current_user_id


router = APIRouter(
    prefix="/api/containers",
    tags=["containers"],
    dependencies=[Depends(get_current_user_id)],
)


@router.get("", response_model=list[SContainerOut])
async def search_containers(
    session: SessionDep,
    q: Annotated[str | None, Query(min_length=1, max_length=11)] = None,
):
    service = ContainersService(ContainersRepository(session))
    return await service.list_or_search(q)


@router.get("/by-cost", response_model=list[SContainerOut])
async def search_by_cost(
    session: SessionDep,
    cost: Decimal | None = Query(default=None, gt=0),
    min: Decimal | None = Query(default=None, gt=0, alias="min"),
    max: Decimal | None = Query(default=None, gt=0, alias="max"),
):
    service = ContainersService(ContainersRepository(session))
    return await service.by_cost(cost, min, max)


@router.post("", response_model=SContainerOut, status_code=status.HTTP_201_CREATED)
async def create_container(
    session: SessionDep,
    payload: SContainerCreate
):
    service = ContainersService(ContainersRepository(session))
    return await service.create(payload)
