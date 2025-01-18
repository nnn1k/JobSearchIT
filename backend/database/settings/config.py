from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    @property
    def ASYNC_DB_URL(self):
        return 'postgresql+asyncpg://mayvwrto:r2avBxAmtEhvx7-LLfTekKidIs0VTOl8@mouse.db.elephantsql.com/mayvwrto'


settings = Settings()
