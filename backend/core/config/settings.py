from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class HostConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class DBConfig(BaseModel):
    url: str = "postgresql+psycopg://postgres.ljkbzaekkpckwgabcekt:jobsearchit@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"
    local_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'


class EmailConfig(BaseModel):
    login: str = 'testemailsendnnn1k@gmail.com'
    password: str = 'tfuu xkwb ccix gnna'


class RedisConfig(BaseModel):
    url: str = 'redis://default:UWNrSrlaQaMQNzMMPJhPmSrrVEysaLUX@switchyard.proxy.rlwy.net:39467'


class JWTConfig(BaseModel):
    private_key: str = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key: str = BASE_DIR / 'certs' / 'jwt-public.pem'


class Settings(BaseSettings):
    run: HostConfig = HostConfig()
    db: DBConfig = DBConfig()
    email: EmailConfig = EmailConfig()
    redis: RedisConfig = RedisConfig()
    jwt: JWTConfig = JWTConfig()


settings = Settings()
