from pydantic import BaseModel
from pydantic_settings import BaseSettings


class HostConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class DBConfig(BaseModel):
    url: str = 'postgresql+asyncpg://postgres:HXjGMYSHgliDTHdJyjPWuXYunubKtacO@monorail.proxy.rlwy.net:52369/railway'

class EmailConfig(BaseModel):
    login: str = 'testemailsendnnn1k@gmail.com'
    password: str = 'znwt bffc blls fpqp'

class RedisConfig(BaseModel):
    url: str = 'redis://default:MXnVzZUbxetVwLWVzvWSTLMIacVdknim@monorail.proxy.rlwy.net:44060'

class Settings(BaseSettings):
    run: HostConfig = HostConfig()
    db: DBConfig = DBConfig()
    email: EmailConfig = EmailConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
