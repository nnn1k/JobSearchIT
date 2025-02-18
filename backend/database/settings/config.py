from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    @property
    def ASYNC_DB_URL(self):
        return 'postgresql+asyncpg://postgres:HXjGMYSHgliDTHdJyjPWuXYunubKtacO@monorail.proxy.rlwy.net:52369/railway'


settings = Settings()
