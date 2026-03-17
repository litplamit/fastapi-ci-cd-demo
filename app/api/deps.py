"""
API Dependencies Module
========================
This module defines reusable dependencies for FastAPI endpoints.
Dependencies are functions that FastAPI calls before executing endpoint logic.

Key concept: Dependency Injection
- FastAPI automatically calls dependency functions
- Results are injected into endpoint parameters
- Promotes code reuse and consistency

Common use cases:
- Database sessions (this file)
- Authentication/authorization
- Rate limiting
- Request validation
"""

from typing import Annotated  # For creating type aliases with metadata

# FastAPI's dependency injection system
from fastapi import Depends

# SQLAlchemy async session type
from sqlalchemy.ext.asyncio import AsyncSession

# Import database session generator
from app.core.database import get_db


# ============================================================================
# TYPE ALIASES (Shortcuts for common dependency patterns)
# ============================================================================

# Create a type alias for database session dependency
# This is a shorthand to avoid repeating the same pattern everywhere
SessionDep = Annotated[AsyncSession, Depends(get_db)]

# What this means:
# - AsyncSession: The type of object returned
# - Depends(get_db): FastAPI should call get_db() to get the session
# - Annotated: Combines type hint with dependency metadata

# Usage comparison:
# 
# WITHOUT SessionDep (verbose):
#   async def read_users(session: AsyncSession = Depends(get_db)):
#       ...
#
# WITH SessionDep (concise):
#   async def read_users(session: SessionDep):
#       ...
#
# Both are identical, but SessionDep is:
# - Shorter and cleaner
# - Consistent across all endpoints
# - Easier to change (update in one place)

