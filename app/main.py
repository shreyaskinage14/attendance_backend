from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.core.database import Base, engine
from app.api.v1.routes import user, attendance, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# Add JWT Bearer Auth globally
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Attendance Management API",
        version="1.0",
        description="API for managing attendance with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Apply BearerAuth globally to every path (except /auth/login and /auth/logout)
    for path, path_item in openapi_schema["paths"].items():
        for method in path_item:
            if not path.startswith("/api/v1/auth/login") and not path.startswith("/api/v1/auth/logout"):
                path_item[method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
