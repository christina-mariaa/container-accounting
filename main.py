from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.containers import router as container_router
from fastapi.openapi.utils import get_openapi

app = FastAPI()
app.include_router(user_router)
app.include_router(container_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Container Accounting API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # По умолчанию все ручки будут требовать Bearer
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi
