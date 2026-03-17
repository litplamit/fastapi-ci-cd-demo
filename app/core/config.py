"""
Application Configuration Module
=================================
This module handles loading and validating environment variables from .env file.
It uses Pydantic for automatic validation and type checking.

Key features:
- Loads credentials from .env file (never hardcode passwords!)
- Validates all required fields are present
- Builds database connection string automatically
- Provides type-safe access to configuration

Security: This file reads sensitive data but never exposes it in logs.
"""

import secrets  # For generating secure random strings (not used currently)
from typing import Any, Dict, List, Optional, Union  # Type hints for better code clarity

# Pydantic imports for validation
from pydantic import AnyHttpUrl, MySQLDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


# ============================================================================
# SETTINGS CLASS
# ============================================================================

class Settings(BaseSettings):
    """
    Application Settings
    
    This class defines all configuration variables needed by the application.
    Pydantic automatically loads values from .env file and validates them.
    
    Required environment variables:
    - PROJECT_NAME: Name of the application
    - MYSQL_SERVER: Database host (e.g., localhost)
    - MYSQL_USER: Database username
    - MYSQL_PASSWORD: Database password
    - MYSQL_DB: Database name
    - MYSQL_PORT: Database port (e.g., 3306)
    """
    
    # Application settings
    PROJECT_NAME: str  # Required: Application name
    API_V1_STR: str = "/api/v1"  # Default: API version prefix
    
    # Database credentials (all required from .env)
    MYSQL_SERVER: str      # Database host (e.g., localhost, IP, or domain)
    MYSQL_USER: str        # Database username
    MYSQL_PASSWORD: str    # Database password (kept secure in .env)
    MYSQL_DB: str          # Database name
    MYSQL_PORT: int        # Database port (typically 3306 for MySQL)
    
    # Database connection URI (auto-generated from above fields)
    SQLALCHEMY_DATABASE_URI: Union[Optional[MySQLDsn], Optional[str]] = None

    # ========================================================================
    # CUSTOM VALIDATORS
    # ========================================================================

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        """
        Build database connection string from individual components.
        
        This validator runs before the Settings object is created.
        It takes individual database credentials and combines them into
        a complete connection string.
        
        Args:
            v: Existing value (if SQLALCHEMY_DATABASE_URI is already set)
            info: ValidationInfo containing all field values
            
        Returns:
            MySQLDsn: Complete database connection URL
            
        Example output:
            mysql+aiomysql://root:password@localhost:3306/myfastapi
        """
        # If connection string is already provided, use it as-is
        if isinstance(v, str):
            return v
        
        # Build connection string from individual components
        return MySQLDsn.build(
            scheme="mysql+aiomysql",  # Use async MySQL driver (aiomysql)
            username=info.data.get("MYSQL_USER"),      # Database username
            password=info.data.get("MYSQL_PASSWORD"),  # Database password
            host=info.data.get("MYSQL_SERVER"),        # Database host
            port=info.data.get("MYSQL_PORT"),          # Database port
            path=f"{info.data.get('MYSQL_DB') or ''}",  # Database name
        )

    # ========================================================================
    # PYDANTIC CONFIGURATION
    # ========================================================================

    model_config = SettingsConfigDict(
        env_file=".env",        # Read from .env file in project root
        case_sensitive=True,    # MYSQL_USER ≠ mysql_user (case matters)
        extra="ignore"          # Ignore unknown variables in .env
    )


# ============================================================================
# GLOBAL SETTINGS INSTANCE
# ============================================================================

# Create a single settings instance that's used throughout the application
# This runs when the module is imported, loading .env and validating all fields
settings = Settings()

# If any required field is missing or invalid, Pydantic will raise an error here
# This ensures the application never starts with invalid configuration

