from backend.core.schemas.models.other.chat_schema import ChatSchema
from backend.core.schemas.models.worker.worker_schema import WorkerSchemaRel, WorkerSchema
from backend.core.schemas.models.worker.resume_schema import ResumeSchema, ResumeSchemaRel
from backend.core.schemas.models.employer.company_schema import CompanySchema, CompanySchemaRel
from backend.core.schemas.models.employer.employer_schema import EmployerSchemaRel, EmployerSchema
from backend.core.schemas.models.employer.vacancy_schema import VacancySchema, VacancySchemaRel
from backend.core.schemas.models.other.response_schema import ResponseSchema, ResponseSchemaRel
from backend.core.schemas.models.other.skill_schema import SkillSchema
from backend.core.schemas.models.other.profession_schema import ProfessionSchema


WorkerSchemaRel.model_rebuild()
ResumeSchema.model_rebuild()
ResumeSchemaRel.model_rebuild()
EmployerSchemaRel.model_rebuild()
CompanySchema.model_rebuild()
VacancySchema.model_rebuild()
VacancySchemaRel.model_rebuild()
ResponseSchema.model_rebuild()
ResponseSchemaRel.model_rebuild()
ChatSchema.model_rebuild()
CompanySchemaRel.model_rebuild()
