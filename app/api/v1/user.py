"""
User API Endpoints (Version 1)
===============================
This module defines all user-related API endpoints for version 1 of the API.
All routes in this file will be prefixed with /api/v1 (configured in main.py).

Available endpoints:
- GET  /api/v1/users  - Retrieve list of users (with pagination)
- POST /api/v1/users  - Create a new user

Architecture pattern:
- Router: Groups related endpoints
- Schemas: Validate request/response data (Pydantic)
- CRUD: Database operations (business logic)
- Models: Database table definitions (SQLAlchemy)
"""

from typing import List  # For type hints (List of users)

# FastAPI components
from fastapi import APIRouter, Depends  # Router for grouping endpoints
from sqlalchemy.ext.asyncio import AsyncSession  # Database session type

# Import dependencies
from app.api.deps import SessionDep  # Database session dependency
from app.crud import user as crud_user  # CRUD operations for users
from app.schemas.user import UserRead, UserCreate  # Pydantic schemas


# ============================================================================
# ROUTER INITIALIZATION
# ============================================================================

# Create router for user endpoints
# This groups all user-related routes together
router = APIRouter()

# This router will be registered in main.py with:
# - Prefix: /api/v1
# - Tags: ["users"]


# ============================================================================
# GET ENDPOINTS
# ============================================================================

@router.get("/users", response_model=List[UserRead])
async def read_users(
    session: SessionDep,  # Database session (auto-injected by FastAPI)
    skip: int = 0,        # Pagination: number of records to skip
    limit: int = 100,     # Pagination: maximum records to return
):
    """
    Retrieve users from database with pagination.
    
    This endpoint fetches a list of users from the database.
    It supports pagination through skip and limit parameters.
    
    Request:
        GET /api/v1/users?skip=0&limit=10
        
    Query Parameters:
        skip (int): Number of records to skip (default: 0)
                   Example: skip=10 starts from the 11th record
        limit (int): Maximum number of records to return (default: 100)
                    Example: limit=10 returns at most 10 users
    
    Response:
        200 OK: List of user objects
        Example:
        [
            {
                "name": "John Doe",
                "user_login_id": 1,
                "user_name": "john",
                "emp_code": "EMP001",
                "driver_onboard_stage_tc": null
            }
        ]
    
    Flow:
        1. FastAPI receives request
        2. Validates query parameters (skip, limit must be integers)
        3. Calls get_db() to create database session
        4. Injects session into this function
        5. Calls CRUD function to fetch users
        6. Validates response against UserRead schema
        7. Converts to JSON and returns
        8. Closes database session automatically
    
    Args:
        session: Database session (injected by FastAPI)
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        
    Returns:
        List[UserRead]: List of user objects matching the schema
    """
    # Call CRUD function to fetch users from database
    # This separates business logic from API layer
    users = await crud_user.get_users(session, skip=skip, limit=limit)
    
    # Return users (FastAPI auto-converts to JSON)
    # Response is validated against List[UserRead] schema
    return users


# ============================================================================
# POST ENDPOINTS
# ============================================================================

@router.post("/users", response_model=UserRead)
async def create_user(
    *,  # Force all parameters after this to be keyword-only
    session: SessionDep,  # Database session (auto-injected)
    user_in: UserCreate,  # Request body (auto-validated by Pydantic)
):
    """
    Create a new user in the database.
    
    This endpoint accepts user data in the request body,
    validates it, and creates a new user record in the database.
    
    Request:
        POST /api/v1/users
        Content-Type: application/json
        
        Body:
        {
            "name": "John Doe",
            "user_login_id": 123,
            "email": "john@example.com"
        }
    
    Response:
        200 OK: Created user object
        Example:
        {
            "name": "John Doe",
            "user_login_id": 123,
            "user_name": "john",
            "emp_code": null,
            "driver_onboard_stage_tc": null
        }
        
        422 Unprocessable Entity: Validation error
        Example:
        {
            "detail": [
                {
                    "loc": ["body", "email"],
                    "msg": "value is not a valid email address",
                    "type": "value_error.email"
                }
            ]
        }
    
    Validation:
        - name: Required, must be a string
        - user_login_id: Required, must be an integer
        - email: Required, must be valid email format
        
    Flow:
        1. FastAPI receives POST request
        2. Parses JSON body
        3. Validates against UserCreate schema
        4. If invalid, returns 422 error with details
        5. If valid, creates database session
        6. Calls CRUD function to create user
        7. Validates response against UserRead schema
        8. Returns created user as JSON
        9. Closes database session
    
    Args:
        session: Database session (injected by FastAPI)
        user_in: User data from request body (validated by Pydantic)
        
    Returns:
        UserRead: Created user object
        
    Raises:
        422: If request body doesn't match UserCreate schema
        500: If database operation fails
    """
    # Call CRUD function to create user in database
    # This handles the actual database INSERT operation
    user = await crud_user.create_user(session, user=user_in)
    
    # Return created user (FastAPI auto-converts to JSON)
    # Response is validated against UserRead schema
    return user

