from authx import AuthX, AuthXConfig,  TokenPayload
from fastapi import Depends, HTTPException, status
from app.config import settings


config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_ALGORITHM=settings.JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRES=60 * settings.JWT_ACCESS_EXPIRES_MIN,
    JWT_REFRESH_TOKEN_EXPIRES=60 * 60 * 24 * settings.JWT_REFRESH_EXPIRES_DAYS,
    JWT_TOKEN_LOCATION=("headers",),
)

auth = AuthX(config)


async def get_optional_token(request: Request) -> Optional[TokenPayload]:
    """Возвращает токен если есть, иначе None"""
    try:
        return await auth.access_token_required(request)
    except HTTPException:
        return None
    except Exception:
        return None


def get_current_user_id(token: Optional[TokenPayload] = Depends(get_optional_token)) -> int:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Обработка токена
    sub = getattr(token, "sub", None) or getattr(token, "subject", None)
    if sub is None and isinstance(token, dict):
        sub = token.get("sub") or token.get("subject")

    try:
        return int(sub)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
        )
