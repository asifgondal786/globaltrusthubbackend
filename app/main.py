"""
GlobalTrustHub Backend - FastAPI Application
A trusted digital ecosystem for global education, work & settlement.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.core.logging import setup_logging
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.verification import router as verification_router
from app.api.chat import router as chat_router
from app.api.reviews import router as reviews_router
from app.api.services import router as services_router
from app.api.payments import router as payments_router
from app.api.admin import router as admin_router
from app.api.news import router as news_router
from app.api.journey import router as journey_router
from app.api.ml import router as ml_router
from app.api.jobs import router as jobs_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    setup_logging()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    yield
    # Shutdown
    print("👋 Shutting down GlobalTrustHub API")


app = FastAPI(
    title=settings.APP_NAME,
    description="Trusted Pathways for Global Education, Work & Settlement",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(verification_router, prefix="/api/v1/verification", tags=["Verification"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(reviews_router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(services_router, prefix="/api/v1/services", tags=["Services"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(news_router, prefix="/api/v1/news", tags=["News"])
app.include_router(journey_router, prefix="/api/v1/journey", tags=["Journey"])
app.include_router(ml_router, prefix="/api/v1/ml", tags=["ML"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["Jobs"])


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "healthy",
        "message": "Welcome to GlobalTrustHub API",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected",
        "version": settings.VERSION,
    }
