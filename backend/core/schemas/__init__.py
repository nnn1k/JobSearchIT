from backend.core.schemas.models.worker.worker_schema import WorkerResponseSchema
from backend.core.schemas.models.worker.resume_schema import ResumeSchema
from backend.core.schemas.models.employer.company_schema import CompanySchema
from backend.core.schemas.models.employer.employer_schema import EmployerResponseSchema
from backend.core.schemas.models.employer.vacancy_schema import VacancySchema
from backend.core.schemas.models.other.response_schema import ResponseSchema
from backend.core.schemas.models.other.skill_schema import SkillSchema
from backend.core.schemas.models.other.profession_schema import ProfessionSchema


WorkerResponseSchema.model_rebuild()
ResumeSchema.model_rebuild()
EmployerResponseSchema.model_rebuild()
CompanySchema.model_rebuild()
VacancySchema.model_rebuild()
ResponseSchema.model_rebuild()
