from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    Server: str = ''
    Database: str = ''
    login: str = ''
    password: str = ''

    @property
    def ASYNC_DB_URL(self):
        return 'postgresql+asyncpg://mayvwrto:r2avBxAmtEhvx7-LLfTekKidIs0VTOl8@mouse.db.elephantsql.com/mayvwrto'

settings = Settings()