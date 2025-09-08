# Create Virtual env
```
    python -m venv .venv
```

# Activate env
.\.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run application
uvicorn steam.main:app --reload

# alembic setup
alembic init alembic
alembic revision --autogenerate -m "db change comment"
alembic upgrade head

# docker mysql setup
