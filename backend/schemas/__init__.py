from .worker_schema import WorkerResponseSchema
from .resume_schema import ResumeSchema
from .skill_schema import SkillSchema
from .company_schema import CompanySchema
from .employer_schema import EmployerResponseSchema
from .vacancy_schema import VacancySchema


WorkerResponseSchema.model_rebuild()
ResumeSchema.model_rebuild()
EmployerResponseSchema.model_rebuild()
CompanySchema.model_rebuild()
VacancySchema.model_rebuild()
