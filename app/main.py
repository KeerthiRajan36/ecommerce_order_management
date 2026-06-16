from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.database import engine, Base
from app.routers.auth import router as auth_router
from app.routers.customers import router as customers
from app.routers.products import router as products
from app.routers.orders import router as orders
from app.routers.shipments import router as shipments
 
from app.utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up...")
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="E-Commerce Order Management System API",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Versioning
api_prefix = settings.API_V1_PREFIX

# Routes
app.include_router(auth_router, prefix=api_prefix)
app.include_router(customers, prefix=api_prefix)
app.include_router(products, prefix=api_prefix)
app.include_router(orders, prefix=api_prefix)
app.include_router(shipments, prefix=api_prefix)


@app.get("/")
async def root():
    return {
        "message": "Welcome to E-Commerce API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )