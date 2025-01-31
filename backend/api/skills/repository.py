from backend.api.skills.schemas import SkillSchema
from backend.database.models.other import SkillsOrm
from backend.database.utils.repository import AlchemyRepository


class SkillsRepository(AlchemyRepository):
    db_model = SkillsOrm
    schema = SkillSchema
