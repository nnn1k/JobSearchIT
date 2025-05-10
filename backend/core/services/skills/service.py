from backend.core.services.skills.repository import SkillRepository


class SkillService:
    def __init__(self, skill_repo: SkillRepository):
        self.skill_repo = skill_repo
