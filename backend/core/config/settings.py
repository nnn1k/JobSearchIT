from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class HostConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class DBConfig(BaseModel):
    old_url: str = 'postgresql+asyncpg://postgres:HXjGMYSHgliDTHdJyjPWuXYunubKtacO@monorail.proxy.rlwy.net:52369/railway'
    url: str = 'postgresql+asyncpg://uetsmlt6w7urp4vkpyl6:OSstQLpWMTmpj7x9CS5RgjElMUezgs@bexamlk0jsmsiil98ui5-postgresql.services.clever-cloud.com:50013/bexamlk0jsmsiil98ui5'
    local_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'


class EmailConfig(BaseModel):
    login: str = 'testemailsendnnn1k@gmail.com'
    password: str = 'znwt bffc blls fpqp'


class RedisConfig(BaseModel):
    url: str = 'redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060'


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
