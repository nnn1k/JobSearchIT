from backend.api.skills.schemas import SkillSchema
from backend.database.models.other import SkillsOrm
from backend.database.utils.repository import AlchemyRepository


class SkillsRepository(AlchemyRepository):
    db_model = SkillsOrm
    schema = SkillSchema

def get_skills_repo():
    return SkillsRepository()

async def get_all_skills():
    skills_repo = get_skills_repo()
    skills = await skills_repo.get_all()
    return skills
