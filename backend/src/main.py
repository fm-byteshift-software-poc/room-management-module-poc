from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # IMPORTANT: Import models BEFORE creating tables
    # This registers models in Base.metadata so create_all() can find them
    from src.models import room_type, reservation, room  # noqa: F401
    
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    # No final do lifespan, após create_all():
    import logging
    logger = logging.getLogger("uvicorn.error")
    logger.info(f"Tables created: {Base.metadata.tables.keys()}")
    
    # Seed initial data
    from src.utils.seed import run_seed
    run_seed()
    
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        title="Room Management Module PoC",
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router with version prefix
    from src.routes import router as api_router
    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_app()