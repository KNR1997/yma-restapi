Here are the correct commands for setting up and running your FastAPI application locally:

## 1. Create Virtual Environment
```bash
python -m venv .venv
```

## 2. Activate Virtual Environment
**For Windows:**
```bash
.venv\Scripts\activate
```

**For macOS/Linux:**
```bash
source .venv/bin/activate
```

## 3. Install Requirements
```bash
pip install -r requirements.txt
```

## 4. Run Application (Correct Command)
```bash
uvicorn yma.main:app --reload --host 0.0.0.0 --port 8080
```

## 5. Alembic Setup & Database Migrations
```bash
# Initialize alembic (only needed once)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "db change comment"

# Apply migrations
alembic upgrade head
```

## Complete Step-by-Step Workflow:
```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
uvicorn yma.main:app --reload --host 0.0.0.0 --port 8080

# 4. In a new terminal (with venv activated), run alembic commands
alembic init alembic          # Only if not already initialized
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## After running, access your application at:
- **API Documentation (Swagger UI):** http://localhost:8080/docs
- **ReDoc Documentation:** http://localhost:8080/redoc
- **Raw OpenAPI JSON:** http://localhost:8080/openapi.json

The key correction is using `uvicorn` before `yma.main:app` - this is the proper way to start a FastAPI application with uvicorn server.