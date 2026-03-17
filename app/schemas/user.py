"""
User Pydantic Schemas
======================
This module defines Pydantic models for request/response validation.
Schemas ensure data integrity and provide automatic API documentation.

Key concepts:
- Pydantic: Data validation library using Python type hints
- BaseModel: Base class for all Pydantic models
- Validation: Automatic type checking and format validation
- Serialization: Convert between Python objects and JSON

Schema types:
- UserBase: Shared fields for all user schemas
- UserCreate: Input schema for creating users (POST requests)
- UserRead: Output schema for returning users (GET responses)
"""

from typing import Optional  # For fields that can be None/null

# Pydantic imports for validation
from pydantic import BaseModel, EmailStr, ConfigDict


# ============================================================================
# BASE SCHEMA (Shared fields)
# ============================================================================

class UserBase(BaseModel):
    """
    Base schema with fields common to all user operations.
    
    This is inherited by other schemas to avoid duplication.
    Only contains fields that are always present and required.
    
    Fields:
        name (str): User's full name (required)
    """
    name: str  # Required field: must be provided and must be a string


# ============================================================================
# INPUT SCHEMAS (Request validation)
# ============================================================================

class UserCreate(UserBase):
    """
    Schema for creating a new user (POST /api/v1/users).
    
    This schema validates the request body when creating a user.
    It inherits 'name' from UserBase and adds additional required fields.
    
    Request example:
        POST /api/v1/users
        {
            "name": "John Doe",
            "user_login_id": 123,
            "email": "john@example.com"
        }
    
    Validation:
        - name: Required string (from UserBase)
        - user_login_id: Required integer
        - email: Required valid email address
    
    If validation fails, FastAPI returns 422 error with details.
    """
    user_login_id: int  # Required: User's unique ID (must be integer)
    email: EmailStr     # Required: Valid email format (validated by Pydantic)
    
    # Why EmailStr?
    # - Automatically validates email format
    # - Rejects invalid emails like "notanemail" or "missing@domain"
    # - Example valid: "user@example.com"
    # - Example invalid: "user@" or "@example.com"


# ============================================================================
# OUTPUT SCHEMAS (Response serialization)
# ============================================================================

class UserRead(UserBase):
    """
    Schema for returning user data (GET /api/v1/users).
    
    This schema defines what fields are included in API responses.
    It inherits 'name' from UserBase and adds all database fields.
    
    Response example:
        GET /api/v1/users
        [
            {
                "name": "John Doe",
                "user_login_id": 123,
                "user_name": "john",
                "emp_code": "EMP001",
                "driver_onboard_stage_tc": null
            }
        ]
    
    Optional fields:
        Fields marked Optional[str] can be null in the response.
        This matches the database where these columns are nullable.
    """
    user_login_id: int  # Required: User's unique ID
    
    # Optional fields (can be null/None)
    user_name: Optional[str] = None  # Username (extracted from email)
    emp_code: Optional[str] = None   # Employee code (may not be set)
    driver_onboard_stage_tc: Optional[str] = None  # Onboarding stage
    is_dob_check: Optional[str] = None  # DOB check status
    
    # Why Optional?
    # - Database allows NULL for these columns
    # - If NULL in database, Pydantic converts to None in Python
    # - None is serialized as null in JSON response
    
    # Pydantic configuration
    model_config = ConfigDict(from_attributes=True)
    # from_attributes=True allows creating this schema from SQLAlchemy models
    # Example:
    #   db_user = User(name="John", user_login_id=1)
    #   user_read = UserRead.from_orm(db_user)  # Works!


# ============================================================================
# SCHEMA SEPARATION BENEFITS
# ============================================================================

# Why separate UserCreate and UserRead?
#
# 1. Security:
#    - Don't expose sensitive fields in responses
#    - Control what clients can send vs. what they receive
#
# 2. Flexibility:
#    - Input and output can have different fields
#    - UserCreate requires email, UserRead doesn't include it
#
# 3. Validation:
#    - Different validation rules for input vs. output
#    - Input: strict validation (reject invalid data)
#    - Output: flexible (handle database nulls)
#
# 4. Documentation:
#    - Swagger UI shows different schemas for requests and responses
#    - Clear API contract for clients

# ============================================================================
# VALIDATION EXAMPLES
# ============================================================================

# VALID UserCreate:
# UserCreate(name="John", user_login_id=1, email="john@example.com")
# ✓ All required fields present
# ✓ email is valid format

# INVALID UserCreate:
# UserCreate(name="John", user_login_id=1, email="invalid")
# ✗ email is not valid format
# → FastAPI returns 422 error

# UserCreate(name="John", user_login_id="abc", email="john@example.com")
# ✗ user_login_id must be integer, not string
# → FastAPI returns 422 error

# VALID UserRead:
# UserRead(name="John", user_login_id=1, emp_code=None)
# ✓ Optional fields can be None

# UserRead(name="John", user_login_id=1)
# ✓ Optional fields default to None if not provided

