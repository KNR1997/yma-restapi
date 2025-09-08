import base64
import logging
import os
from urllib import parse

from pydantic import BaseModel
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

log = logging.getLogger(__name__)


class BaseConfigurationModel(BaseModel):
    pass


def get_env_tags(tag_list: list[str]) -> dict:
    """Create dictionary of available env tags."""
    tags = {}
    for t in tag_list:
        tag_key, env_key = t.split(":")

        env_value = os.environ.get(env_key)

        if env_value:
            tags.update({tag_key: env_value})

    return tags


config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
DISPATCH_AUTHENTICATION_PROVIDER_SLUG = config(
    "DISPATCH_AUTHENTICATION_PROVIDER_SLUG", default="dispatch-auth-provider-basic"
)
DISPATCH_AUTHENTICATION_DEFAULT_USER = config(
    "DISPATCH_AUTHENTICATION_DEFAULT_USER", default="dispatch@example.com"
)
DISPATCH_JWT_SECRET = config("DISPATCH_JWT_SECRET", default="secret-key")
DISPATCH_JWT_ALG = config("DISPATCH_JWT_ALG", default="HS256")
DISPATCH_JWT_EXP = config("DISPATCH_JWT_EXP", cast=int, default=86400)  # Seconds
