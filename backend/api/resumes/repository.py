from backend.api.resumes.schemas import ResumeSchema
from backend.database.models.worker import ResumesOrm
from backend.database.utils.repository import AlchemyRepository


class ResumesRepository(AlchemyRepository):
    db_model = ResumesOrm
    schema = ResumeSchema

def get_resume_repo():
    return ResumesRepository()

