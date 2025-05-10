from backend.core.schemas import ProfessionSchema
from backend.core.services.professions.repository import ProfessionRepository


class ProfessionService:
    def __init__(self, prof_repo: ProfessionRepository):
        self.prof_repo = prof_repo

    async def get_professions(self, **kwargs):
        professions = await self.prof_repo.get_professions(**kwargs)
        return [ProfessionSchema.model_validate(pr, from_attributes=True) for pr in professions]
