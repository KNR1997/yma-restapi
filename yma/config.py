import os
import logging
from dotenv import load_dotenv

from starlette.config import Config

log = logging.getLogger(__name__)


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

TORTOISE_ORM = {
    "connections": {
        "default": f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    },
    "apps": {
        "models": {
            # include all your domain model modules
            "models": [
                "yma.auth.models",
                "yma.subject.models",
                "yma.course.models",
                "yma.hall.models",
                "yma.event.models",
                "yma.guardian.models",
                "yma.student.models",
                "yma.enrollment.models",
                "yma.api_log.models",
                "yma.payments.models",
                "aerich.models"  # 👈 Aerich needs this
            ],
            "default_connection": "default",
        },
    },
}

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
YMA_JWT_SECRET = config("YMA_JWT_SECRET", default="secret-key")
YMA_JWT_ALG = config("YMA_JWT_ALG", default="HS256")
YMA_JWT_EXP = config("YMA_JWT_EXP", cast=int, default=86400)  # Seconds
