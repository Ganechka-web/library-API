from os import path, getenv
from pathlib import Path

import dotenv


# project root dir
BASE_DIR = Path(__file__).parent.parent.parent

dotenv.load_dotenv(path.join(BASE_DIR, '.env'))


class PostgresSettings:
    host: str = getenv('POSTGRES_HOST')
    port: int = getenv('POSTGRES_PORT')
    user: str = getenv('POSTGRES_USER')
    password: str = getenv('POSTGRES_PASS')
    db: str = getenv('POSTGRES_DB')


postgres_settings = PostgresSettings()
