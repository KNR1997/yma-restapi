<p align="center">
<a href="https://fastapi.tiangolo.com" target="_blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="400"></a>
</p>

### Features

- **Popular Tech Stack**: The backend is developed with the high-performance asynchronous framework FastAPI using Python 3.11, while the front-end is powered by cutting-edge technologies such as Vue3 and Vite, complemented by the efficient package manager, pnpm.
- **Code Standards**: The project is equipped with various plugins for code standardization and quality control, ensuring consistency and enhancing team collaboration efficiency.
- **JWT Authentication**: User identity verification and authorization are handled through JWT, enhancing the application's security.


### ⚡️ How to install

1. Create and activate virtual environment
```sh
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.\.venv\Scripts\activate  # Windows
```

2. Install requirements
```sh
pip install -r requirements.txt
```

3. cp .env.template .env

4. Start the backend service
```sh
uvicorn yma.main:app --reload --host 0.0.0.0 --port 8080
```


### ⚡️ DB migration steps
alembic init alembic
alembic revision --autogenerate -m "db change comment"
alembic upgrade head

# docker mysql setup
