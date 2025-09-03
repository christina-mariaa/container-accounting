from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

CONTAINER_PATTERN = r"^[A-Z]{3}U\d{7}$"


class SUserLogin(BaseModel):
    username: str
    password: str


class SUserCreate(BaseModel):
    username: str
    password: str = Field(min_length=8, max_length=128)


class SAuthAccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SAuthTokensPair(SAuthAccessToken):
    refresh_token: str


class SContainerOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    container_number: str
    cost: Decimal


class SContainerCreate(BaseModel):
    container_number: str = Field(pattern=CONTAINER_PATTERN)
    cost: Decimal = Field(gt=0)

    @field_validator("container_number")
    @classmethod
    def _upper_and_check(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("cost")
    @classmethod
    def _two_decimals(cls, v: Decimal) -> Decimal:
        if v.as_tuple().exponent < -2:
            raise ValueError("cost must have at most two decimal places")
        return v
