"""
FastAPI Application Entry Point
================================
This is the main file that creates and configures the FastAPI application.
It serves as the entry point when running: uvicorn app.main:app --reload

Key responsibilities:
- Create the FastAPI application instance
- Register API routers (endpoints)
- Configure application metadata (title, OpenAPI URL)
- Define root-level endpoints

Author: Amit
Date: 2026-01-07
"""

# Import FastAPI framework - the core web framework
from fastapi import FastAPI

# Import application settings (loaded from .env file)
from app.core.config import settings

# Import user router containing all user-related API endpoints
from app.api.v1 import user

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

# Create FastAPI application instance
# This is the main application object that handles all HTTP requests
app = FastAPI(
    title=settings.PROJECT_NAME,  # Application name (shown in Swagger docs)
    openapi_url=f"{settings.API_V1_STR}/openapi.json",  # OpenAPI schema URL
)

# ============================================================================
# ROUTER REGISTRATION
# ============================================================================

# Register user router with the application
# This adds all user endpoints under the /api/v1 prefix
# Example: GET /api/v1/users, POST /api/v1/users
app.include_router(
    user.router,                    # Router object containing user endpoints
    prefix=settings.API_V1_STR,     # Add /api/v1 prefix to all routes
    tags=["users"]                  # Group endpoints under "users" in docs
)

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
def read_root():
    """
    Root endpoint - Health check
    
    Returns a welcome message to verify the API is running.
    Accessible at: http://localhost:8000/
    
    Returns:
        dict: Welcome message
    """
    return {"message": "Welcome to MyFASTAPI"}

