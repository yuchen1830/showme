"""
Main FastAPI application
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.routes import router as v1_router
from src.api.logging_config import setup_logging, add_correlation_id_middleware


# Setup structured logging
setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="ShowMe AI Backend",
        description="Ticket aggregation and AI-powered seat map analysis",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add correlation ID middleware
    app.middleware("http")(add_correlation_id_middleware)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Frontend URLs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(v1_router)
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "service": "ShowMe AI Backend",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    return app


# Create app instance
app = create_app()
