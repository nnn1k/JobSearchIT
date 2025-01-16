from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from backend.database.settings.database import Base

class WorkersOrm(Base):
    __tablename__ = 'workers'

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    password: Mapped[str]
    birthday: Mapped[str]
    gender: Mapped[str]
    city: Mapped[str]

    resumes: Mapped[list['ResumesOrm']] = relationship("ResumesOrm", back_populates="worker")
    educations: Mapped[list['EducationsOrm']] = relationship("EducationsOrm", back_populates="worker")
    skills: Mapped[list['SkillsOrm']] = relationship("SkillsOrm", secondary='workers_skills', back_populates="workers")

class ResumesOrm(Base):
    __tablename__ = 'resumes'

    title: Mapped[str]
    description: Mapped[str]
    salary: Mapped[str]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'))

    worker: Mapped[WorkersOrm] = relationship("WorkersOrm", back_populates="resumes")
    responses: Mapped[list['ResponsesOrm']] = relationship("ResponsesOrm", back_populates="resume")

class EducationsOrm(Base):
    __tablename__ = 'educations'

    education_type: Mapped[str]
    end_date: Mapped[str]
    institution: Mapped[str]
    specialization: Mapped[str]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'))

    worker: Mapped[WorkersOrm] = relationship("WorkersOrm", back_populates="educations")

class SkillsOrm(Base):
    __tablename__ = 'skills'

    name: Mapped[str]

    workers: Mapped[list['WorkersOrm']] = relationship("WorkersSkillsOrm", back_populates="skill")
    vacancies: Mapped[list['VacanciesOrm']] = relationship("VacanciesSkillsOrm", back_populates="skill")

class EmployersOrm(Base):
    __tablename__ = 'employers'

    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    password: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))
    is_owner: Mapped[bool]

    company: Mapped['CompaniesOrm'] = relationship("CompaniesOrm", back_populates="employers")

class CompaniesOrm(Base):
    __tablename__ = 'companies'

    name: Mapped[str]
    description: Mapped[str]

    employers: Mapped[list[EmployersOrm]] = relationship("EmployersOrm", back_populates="company")
    vacancies: Mapped[list['VacanciesOrm']] = relationship("VacanciesOrm", back_populates="company")

class VacanciesOrm(Base):
    __tablename__ = 'vacancies'

    title: Mapped[str]
    description: Mapped[str]
    salary: Mapped[str]
    city: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))

    company: Mapped[CompaniesOrm] = relationship("CompaniesOrm", back_populates="vacancies")
    responses: Mapped[list['ResponsesOrm']] = relationship("ResponsesOrm", back_populates="vacancy")
    skills: Mapped[list['SkillsOrm']] = relationship("VacanciesSkillsOrm", back_populates="vacancy")

class ResponsesOrm(Base):
    __tablename__ = 'responses'

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id'))
    resume_id: Mapped[int] = mapped_column(ForeignKey('resumes.id'))

    vacancy: Mapped[VacanciesOrm] = relationship("VacanciesOrm", back_populates="responses")
    resume: Mapped[ResumesOrm] = relationship("ResumesOrm", back_populates="responses")

class VacanciesSkillsOrm(Base):
    __tablename__ = 'vacancies_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.id'))

    skill: Mapped[SkillsOrm] = relationship("SkillsOrm", back_populates="vacancies")
    vacancy: Mapped[VacanciesOrm] = relationship("VacanciesOrm", back_populates="skills")

class WorkersSkillsOrm(Base):
    __tablename__ = 'workers_skills'

    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'))
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id'))

    skill: Mapped[SkillsOrm] = relationship("SkillsOrm", back_populates="workers")
    worker: Mapped[WorkersOrm] = relationship("WorkersOrm", back_populates="skills")

