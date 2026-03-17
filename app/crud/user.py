"""
User CRUD Operations
=====================
This module contains database operations for the User model.
CRUD stands for: Create, Read, Update, Delete

Key concepts:
- Separation of concerns: Database logic separate from API logic
- Async operations: Non-blocking database queries
- SQLAlchemy ORM: Object-oriented database queries
- Reusability: Functions can be used by multiple endpoints

Architecture:
- API endpoints (user.py) call these functions
- These functions interact with database
- Returns Python objects (not JSON)
"""

from typing import Sequence  # Type hint for sequences (like lists)

# SQLAlchemy query builder
from sqlalchemy import select

# Async database session
from sqlalchemy.ext.asyncio import AsyncSession

# Import database model and schema
from app.models.user import User, UserDetail  # SQLAlchemy model (database table)
from app.schemas.user import UserCreate  # Pydantic schema (validation)
from sqlalchemy.orm import selectinload

# ============================================================================
# READ OPERATIONS
# ============================================================================

async def get_users(
    db: AsyncSession,  # Database session (provided by FastAPI)
    skip: int = 0,     # Pagination: records to skip
    limit: int = 100     # Pagination: max records to return
) -> Sequence[User]:
    """
    Retrieve users with their details using INNER JOIN.
    
    This function fetches users from the database using SQLAlchemy's
    async ORM. It supports pagination through skip and limit parameters.
    
    SQL equivalent:
        SELECT u.*, ud.*
        FROM user_login u
        INNER JOIN user_login_detail ud ON u.user_login_id = ud.user_login_id
        OFFSET {skip} LIMIT {limit}
    
    Args:
        db: Async database session
        skip: Number of records to skip (default: 0)
              Example: skip=10 starts from 11th record
        limit: Maximum records to return (default: 1)
               Example: limit=10 returns at most 10 users
    
    Returns:
        Sequence[User]: List of User model instances
        
    Example:
        users = await get_users(db, skip=0, limit=10)
        for user in users:
            print(user.name, user.user_login_id)
    
    Flow:
        1. Build SELECT query with OFFSET and LIMIT
        2. Execute query asynchronously (await)
        3. Extract User objects from result
        4. Return list of users
    """
    # Build SQL query using SQLAlchemy's select()
    # select(User) = SELECT * FROM user_login
    # .offset(skip) = OFFSET {skip}
    # .limit(limit) = LIMIT {limit}
    stmt = (select(User)
           .join(UserDetail,User.user_login_id == UserDetail.user_login_id)
           .offset(skip).limit(limit))

           

    #.join(UserDetail,User.user_login_id == UserDetail.user_login_id)
    #.join(User.detail)  # INNER JOIN via relationship
    # Execute the query asynchronously
    # await: Wait for database to return results without blocking
    # db.execute(): Send query to database
    result = await db.execute(stmt)
    
    # Extract User objects from result
    # result.scalars(): Get just the User objects (not tuples)
    # .all(): Convert to list
    return result.scalars().all()
    
    # Why scalars()?
    # - Without: result contains Row objects: [(User1,), (User2,)]
    # - With: result contains User objects: [User1, User2]


# ============================================================================
# CREATE OPERATIONS
# ============================================================================

async def create_user(
    db: AsyncSession,   # Database session
    user: UserCreate    # User data (validated by Pydantic)
) -> User:
    """
    Create a new user in the database.
    
    This function takes validated user data (UserCreate schema),
    creates a User model instance, and saves it to the database.
    
    SQL equivalent:
        INSERT INTO user_login (user_login_id, name, user_name)
        VALUES ({user_login_id}, {name}, {user_name})
    
    Args:
        db: Async database session
        user: UserCreate schema with validated user data
              Contains: name, user_login_id, email
    
    Returns:
        User: Created user model instance (with all database fields)
        
    Example:
        user_data = UserCreate(
            name="John Doe",
            user_login_id=123,
            email="john@example.com"
        )
        new_user = await create_user(db, user_data)
        print(new_user.user_login_id)  # 123
        print(new_user.user_name)      # "john"
    
    Flow:
        1. Create User model instance from UserCreate data
        2. Extract username from email
        3. Add to database session (not saved yet)
        4. Commit transaction (save to database)
        5. Refresh to get any database-generated values
        6. Return created user
    """
    # Create User model instance
    # This creates a Python object but doesn't save to database yet
    db_user = User(
        user_login_id=user.user_login_id,  # From UserCreate schema
        name=user.name,                     # From UserCreate schema
        user_name=user.email.split('@')[0]  # Extract username from email
    )
    # Example: "john@example.com" → "john"
    
    # Add user to session
    # This stages the user for insertion but doesn't execute INSERT yet
    db.add(db_user)
    
    # Commit the transaction
    # This executes the INSERT statement and saves to database
    # await: Wait for database to confirm the insert
    await db.commit()
    
    # Refresh the user object
    # This re-fetches the user from database to get any auto-generated values
    # Example: auto-increment IDs, default values, triggers
    await db.refresh(db_user)
    
    # Return the created user
    # This User object can be converted to UserRead schema by FastAPI
    return db_user


# ============================================================================
# IMPORTANT NOTES
# ============================================================================

# 1. Why async/await?
#    - Non-blocking: Server can handle other requests while waiting
#    - Performance: Can handle thousands of concurrent requests
#    - Modern: Industry standard for Python web apps

# 2. Transaction management:
#    - db.add(): Stage changes (not saved yet)
#    - db.commit(): Save changes to database
#    - If error occurs before commit, changes are rolled back

# 3. Error handling:
#    - If commit fails (e.g., duplicate key), exception is raised
#    - FastAPI catches exception and returns 500 error
#    - Database session is automatically rolled back

# 4. Session lifecycle:
#    - Session created by get_db() in database.py
#    - Passed to this function by FastAPI
#    - Automatically closed after request completes
#    - Never manually close session in CRUD functions

# 5. Why separate CRUD from API?
#    - Reusability: Same function can be used by multiple endpoints
#    - Testability: Easy to test database logic independently
#    - Maintainability: Database logic in one place
#    - Flexibility: Easy to add caching, logging, etc.
