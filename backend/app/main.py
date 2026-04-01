from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.routes import auth, projects, tasks, users


def create_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Mini Project Management System",
        version="1.0.0",
        description="FastAPI backend for managing users, projects, and tasks.",
    )

    register_exception_handlers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(projects.router, prefix="/projects", tags=["Projects"])
    app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_application()
