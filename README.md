
# MyFASTAPI
# New Changes1

A production-grade FastAPI application using Async SQLAlchemy, Pydantic, and PostgreSQL.

## Features

- **FastAPI**: Modern, fast (high-performance), web framework for building APIs.
- **Async SQLAlchemy**: Database interaction using asynchronous sessions.
- **Pydantic**: Data validation and settings management using Python type hints.
- **Modular Structure**: Organized by domain and functionality for scalability.
- **Secure Configuration**: Environment variables management with `.env`.

## Requirements

- Python 3.10+
- PostgreSQL DatabaseS

## Installation & Setup

1. **Create a Virtual Environment**:
   ```sh
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   A `.env` file has been created with default values. Update it with your actual database credentials:
   ```ini
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=postgres
   ```
   **Security Note**: Never commit `.env` to version control. It is already added to `.gitignore`.

## Running the Application

1. **Start the Server**:
   ```sh
   uvicorn app.main:app --reload
   ```

2. **Verify Output**:
   You should see output similar to:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   ```

3. **Access Documentation**:
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing the API

1. **Get Users**:
   - Endpoint: `GET /api/v1/users`
   - URL: [http://127.0.0.1:8000/api/v1/users](http://127.0.0.1:8000/api/v1/users)
   - Response: `[]` (Empty list if DB is empty)

2. **Create User** (via Swagger UI or Curl):
   ```sh
   curl -X 'POST' \
     'http://127.0.0.1:8000/api/v1/users' \
     -H 'Content-Type: application/json' \
     -d '{
     "name": "John Doe",
     "email": "john@example.com"
   }'
   ```

## Project Structure

```
MyFASTAPI/
├── app/
│   ├── main.py                # Entry point
│   ├── core/                  # Config & DB
│   ├── models/                # SQLAlchemy Models
│   ├── schemas/               # Pydantic Schemas
│   ├── crud/                  # DB Operations
│   └── api/                   # Routes & Deps
├── .env                       # Secrets
├── .gitignore
└── requirements.txt
```


## Docker Setup

1. **Build the Docker Image**:
   ```sh
   docker build -t myfastapi-api .
   ```

2. **Run the Docker Container**:
   ```sh
   docker run --env-file .env -p 8000:8000 myfastapi-api
   ```
3. **docker compose up**   
   ```sh
   docker compose up
   ```
4. **docker compose down**   
   ```sh
   docker compose down
   ```
