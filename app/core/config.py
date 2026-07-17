from dataclasses import dataclass
from json import loads
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    DATABASE_URL: str
    cors_allow_origins: list[str]


def get_settings():
    return Settings(
        DATABASE_URL=getenv("DATABASE_URL"),
        cors_allow_origins=loads(getenv("cors_allow_origins")),
    )
