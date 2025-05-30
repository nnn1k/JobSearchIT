from typing import Sequence

from sqlalchemy.exc import IntegrityError

from backend.core.schemas import ResponseSchema
from backend.core.schemas.models.other.response_schema import ResponseSchemaRel
from backend.core.services.chats.service import ChatService
from backend.core.services.responses.repository import ResponseRepository
from backend.core.services.resumes.service import ResumeService
from backend.core.services.vacancies.service import VacancyService
from backend.core.utils.const import WORKER_USER_TYPE, EMPLOYER_USER_TYPE
from backend.core.utils.exc import (
    response_is_exist_exc,
    user_is_not_owner_exc,
    incorrect_user_type_exc,
    response_not_found_exc
)
from backend.core.utils.other.type_utils import UserVar


class ResponseService:

    def __init__(
            self,
            resp_repo: ResponseRepository,
            vacancy_serv: VacancyService,
            resume_serv: ResumeService,
            chat_serv: ChatService,
    ):
        self.resp_repo = resp_repo
        self.vacancy_serv = vacancy_serv
        self.resume_serv = resume_serv
        self.chat_serv = chat_serv

    async def send_response(self, user: UserVar, resume_id: int, vacancy_id: int) -> ResponseSchema:
        if await self.check_response_is_exist(resume_id=resume_id, vacancy_id=vacancy_id):
            raise response_is_exist_exc
        if not await self.check_user_is_not_owner(resume_id=resume_id, vacancy_id=vacancy_id, user=user):
            raise user_is_not_owner_exc
        is_worker_accepted = None
        is_employer_accepted = None
        if user.type == WORKER_USER_TYPE:
            is_worker_accepted = True
        elif user.type == EMPLOYER_USER_TYPE:
            is_employer_accepted = True
        try:
            response = await self.resp_repo.send_response(
                resume_id=resume_id,
                vacancy_id=vacancy_id,
                first=user.type,
                is_worker_accepted=is_worker_accepted,
                is_employer_accepted=is_employer_accepted
            )
        except IntegrityError:
            raise response_is_exist_exc
        schema = ResponseSchema.model_validate(response)
        return schema

    async def check_response_is_exist(self, resume_id: int, vacancy_id: int) -> bool:
        response = await self.resp_repo.get_response(resume_id=resume_id, vacancy_id=vacancy_id)
        return bool(response)

    async def check_user_is_not_owner(self, resume_id: int, vacancy_id: int, user: UserVar) -> bool:
        if user.type == WORKER_USER_TYPE:
            resume = await self.resume_serv.get_resume(resume_id=resume_id)
            return user.id == resume.worker_id

        elif user.type == EMPLOYER_USER_TYPE:
            vacancy = await self.vacancy_serv.get_vacancy(vacancy_id=vacancy_id)
            return vacancy.company_id == user.company_id

    async def get_responses(self, user: UserVar) -> Sequence[ResponseSchemaRel]:
        if user.type == WORKER_USER_TYPE:
            responses = await self.resp_repo.get_responses_worker(user_id=user.id)
        elif user.type == EMPLOYER_USER_TYPE:
            responses = await self.resp_repo.get_responses_employer(company_id=user.company_id)
        else:
            raise incorrect_user_type_exc
        return [ResponseSchemaRel.model_validate(resp) for resp in responses]

    async def get_invites(self, user: UserVar) -> Sequence[ResponseSchemaRel]:
        if user.type == WORKER_USER_TYPE:
            responses = await self.resp_repo.get_invites_worker(user_id=user.id)
        elif user.type == EMPLOYER_USER_TYPE:
            responses = await self.resp_repo.get_invites_employer(company_id=user.company_id)
        else:
            raise incorrect_user_type_exc
        return [ResponseSchemaRel.model_validate(resp) for resp in responses]

    async def send_reaction(self, user: UserVar, reaction: bool, response_id: int) -> ResponseSchema:
        response = await self.resp_repo.get_response(id=response_id)
        if not await self.check_user_is_not_owner(
                resume_id=response.resume_id, vacancy_id=response.vacancy_id, user=user
        ):
            raise user_is_not_owner_exc
        if user.type == WORKER_USER_TYPE:
            response = await self.resp_repo.send_reaction_to_response_worker(response_id=response_id, reaction=reaction)
        elif user.type == EMPLOYER_USER_TYPE:
            response = await self.resp_repo.send_reaction_to_response_employer(response_id=response_id, reaction=reaction)
        else:
            raise incorrect_user_type_exc
        if not response:
            raise response_not_found_exc
        schema = ResponseSchema.model_validate(response)
        return schema

    async def delete_response(self, response_id: int, user: UserVar) -> None:
        response = await self.resp_repo.get_response(id=response_id)
        if not await self.check_user_is_not_owner(
                resume_id=response.resume_id, vacancy_id=response.vacancy_id, user=user
        ):
            raise user_is_not_owner_exc
        response = await self.resp_repo.delete_response(response_id=response_id)
        if not response:
            raise response_not_found_exc


