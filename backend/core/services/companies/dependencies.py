from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database.utils.dependencies import get_db
from backend.core.services.companies.repository import CompanyRepository
from backend.core.services.companies.service import CompanyService
from backend.core.services.users.dependencies import get_user_serv
from backend.core.services.users.service import UserService


def get_company_repo(session: AsyncSession = Depends(get_db)):
    return CompanyRepository(session=session)


def get_company_serv(
        company_repo: CompanyRepository = Depends(get_company_repo),
        user_serv: UserService = Depends(get_user_serv),
):
    return CompanyService(company_repo=company_repo, user_serv=user_serv)