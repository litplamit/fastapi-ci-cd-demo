"""
User Database Model
===================
This module defines the User table structure using SQLAlchemy ORM.
It maps Python class to database table, allowing object-oriented database operations.

Key concepts:
- ORM (Object-Relational Mapping): Python objects ↔ Database rows
- Declarative Base: SQLAlchemy's way to define models
- Columns: Define table structure and data types

Table: user_login
Primary Key: user_login_id
"""

# SQLAlchemy column types
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String

# Import Base class (all models inherit from this)
from app.core.database import Base
from sqlalchemy.orm import relationship




class UserDetail(Base):
    __tablename__ = "user_login_details"
    
    # ========================================================================
    # COLUMNS (Table structure)
    # ========================================================================
    
    # Primary key column
    user_login_details_id = Column(
        Integer,           # Data type: whole numbers
        primary_key=True,  # This is the unique identifier for each row
        index=True         # Create index for faster lookups
    )
    # Why index=True?
    # - Speeds up queries that search by user_login_id
    # - Essential for primary keys (automatically indexed anyway)

    user_login_id = Column(
        Integer,           
        ForeignKey("user_login.user_login_id"),  
        nullable=False        
    )
    
    # User's is_dob_check
    is_dob_check = Column(
        String,      # Data type: text/varchar
        index=False  # No index (not frequently searched)
    )
  
    user = relationship("User", back_populates="detail")
    

# ============================================================================
# USER MODEL
# ============================================================================

class User(Base):
    """
    User model representing the user_login table.
    
    This class defines the structure of the user_login table in MySQL.
    Each instance of this class represents one row in the table.
    
    Table name: user_login
    Primary key: user_login_id
    
    Example usage:
        # Create a new user
        new_user = User(
            user_login_id=1,
            name="John Doe",
            user_name="john",
            emp_code="EMP001"
        )
        
        # Access attributes
        print(new_user.name)  # "John Doe"
        print(new_user.user_login_id)  # 1
    """
    
    # Table name in the database
    # This MUST match the actual table name in MySQL
    __tablename__ = "user_login"
    
    # ========================================================================
    # COLUMNS (Table structure)
    # ========================================================================
    
    # Primary key column
    user_login_id = Column(
        Integer,           # Data type: whole numbers
        primary_key=True,  # This is the unique identifier for each row
        index=True         # Create index for faster lookups
    )
    # Why index=True?
    # - Speeds up queries that search by user_login_id
    # - Essential for primary keys (automatically indexed anyway)
    
    # User's full name
    name = Column(
        String,      # Data type: text/varchar
        index=False  # No index (not frequently searched)
    )
    
    # Username (extracted from email or set manually)
    user_name = Column(
        String,         # Data type: text/varchar
        unique=False,   # Multiple users can have same username (not enforced)
        index=False     # No index
    )
    
    # Employee code (optional identifier)
    emp_code = Column(
        String,         # Data type: text/varchar
        unique=False,   # Not unique
        index=False     # No index
    )
    # Note: This column can be NULL in database
    
    # Driver onboarding stage tracking code
    driver_onboard_stage_tc = Column(
        String,         # Data type: text/varchar
        unique=False,   # Not unique
        index=False     # No index
    )
    # Note: This column can be NULL in database

    # Add relationship (optional but recommended)
    detail = relationship("UserDetail", back_populates="user", uselist=False)
    # uselist=False means one-to-one relationship

# ============================================================================
# IMPORTANT NOTES
# ============================================================================

# 1. This model DOES NOT create the table
#    - The table must already exist in MySQL
#    - This just maps Python class to existing table
#    - Use Alembic migrations to create/modify tables

# 2. Column names must match database exactly
#    - user_login_id in Python = user_login_id in MySQL
#    - Case-sensitive depending on database settings

# 3. Missing columns in model
#    - If database has columns not defined here, they're ignored
#    - If model has columns not in database, queries will fail

# 4. Nullable columns
#    - By default, columns allow NULL unless nullable=False
#    - emp_code and driver_onboard_stage_tc can be NULL
