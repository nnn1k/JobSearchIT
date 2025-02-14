from backend.schemas.models.worker.worker_schema import WorkerResponseSchema
from backend.schemas.models.worker.resume_schema import ResumeSchema
from backend.schemas.models.other.skill_schema import SkillSchema
from backend.schemas.models.employer.company_schema import CompanySchema
from backend.schemas.models.employer.employer_schema import EmployerResponseSchema
from backend.schemas.models.employer.vacancy_schema import VacancySchema


WorkerResponseSchema.model_rebuild()
ResumeSchema.model_rebuild()
EmployerResponseSchema.model_rebuild()
CompanySchema.model_rebuild()
VacancySchema.model_rebuild()
