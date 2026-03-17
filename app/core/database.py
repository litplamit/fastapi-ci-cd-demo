"""
Database Connection Manager
============================
This module manages database connections using SQLAlchemy's async engine.
It implements connection pooling for efficient resource usage.

Key concepts:
- Engine: Manages connection pool (created once at startup)
- Session: Individual database connection (created per request)
- Dependency Injection: FastAPI automatically provides sessions to endpoints

Connection lifecycle:
1. Engine created at startup (maintains pool of connections)
2. Per request: get_db() creates a session from the pool
3. After request: session automatically closed and returned to pool
"""

from typing import AsyncGenerator  # Type hint for generator functions

# SQLAlchemy async imports for database operations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Import application settings (contains database connection string)
from app.core.config import settings


# ============================================================================
# DATABASE ENGINE (Connection Pool Manager)
# ============================================================================

# Create async database engine
# This is created ONCE when the application starts
# Think of it as a "parking lot" that manages multiple database connections
engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),  # Connection string from config
    echo=True,       # Log all SQL queries (set to False in production)
    future=True,     # Use SQLAlchemy 2.0 style API
)

# Why async?
# - Non-blocking: Server can handle other requests while waiting for database
# - Performance: Can handle thousands of concurrent requests
# - Modern: Industry standard for Python web applications


# ============================================================================
# SESSION FACTORY (Creates database sessions on demand)
# ============================================================================

# Create session factory
# This is a "factory" that creates new sessions when needed
# Each API request gets its own session from this factory
SessionLocal = async_sessionmaker(
    autocommit=False,           # Don't auto-commit changes (explicit control)
    autoflush=False,            # Don't auto-sync objects to database
    bind=engine,                # Use our engine (connection pool)
    class_=AsyncSession,        # Return AsyncSession objects
    expire_on_commit=False,     # Keep objects usable after commit
)

# Session vs Engine:
# - Engine: Manages the pool (created once)
# - Session: Individual connection from pool (created per request)


# ============================================================================
# DATABASE DEPENDENCY (Provides sessions to API endpoints)
# ============================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency for FastAPI endpoints.
    
    This is a generator function that FastAPI uses for dependency injection.
    It creates a new database session for each request and ensures it's
    properly closed after the request completes.
    
    Usage in endpoints:
        @router.get("/users")
        async def read_users(session: SessionDep):
            # session is automatically provided by FastAPI
            users = await session.execute(select(User))
            return users
    
    Lifecycle:
        1. Request arrives
        2. FastAPI calls get_db()
        3. Session created from pool
        4. Session yielded to endpoint
        5. Endpoint executes
        6. Response sent
        7. Finally block runs (session closed)
        8. Connection returned to pool
    
    Yields:
        AsyncSession: Database session for this request
    """
    # Create a new session from the factory
    async with SessionLocal() as session:
        try:
            # Provide session to the endpoint
            yield session
        finally:
            # This ALWAYS runs, even if an error occurs
            # Ensures connections are never leaked
            await session.close()


# ============================================================================
# BASE CLASS FOR MODELS
# ============================================================================

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base class for all database models.
    
    All database table models inherit from this class.
    It provides common functionality and metadata for SQLAlchemy ORM.
    
    Example usage:
        class User(Base):
            __tablename__ = "users"
            id = Column(Integer, primary_key=True)
            name = Column(String)
    """
    pass

# Why use a Base class?
# - Consistency: All models share common behavior
# - Metadata: SQLAlchemy tracks all models through this base
# - Migrations: Alembic uses this to detect schema changes

