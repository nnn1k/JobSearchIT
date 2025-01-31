import asyncio

from backend.database.settings.database import engine, Base, session_factory
from backend.database.models.worker import WorkersOrm, ResumesOrm, EducationsOrm
from backend.database.models.employer import EmployersOrm, CompaniesOrm, VacanciesOrm
from backend.database.models.other import SkillsOrm, WorkersSkillsOrm, VacanciesSkillsOrm, ResponsesOrm


async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_skills():
    async with session_factory() as session:
        skills = [
            SkillsOrm(name="Python"),
            SkillsOrm(name="Java"),
            SkillsOrm(name="C#"),
            SkillsOrm(name="JavaScript"),
            SkillsOrm(name="Ruby"),
            SkillsOrm(name="PHP"),
            SkillsOrm(name="Go"),
            SkillsOrm(name="Rust"),
            SkillsOrm(name="C++"),
            SkillsOrm(name="Веб-разработка"),
            SkillsOrm(name="Мобильная разработка"),
            SkillsOrm(name="API"),
            SkillsOrm(name="Игровая разработка"),
            SkillsOrm(name="SQL"),
            SkillsOrm(name="NoSQL"),
            SkillsOrm(name="Оптимизация БД"),
            SkillsOrm(name="Администрирование БД"),
            SkillsOrm(name="Docker"),
            SkillsOrm(name="Kubernetes"),
            SkillsOrm(name="Облачные вычисления"),
            SkillsOrm(name="CI/CD"),
            SkillsOrm(name="Автоматизация тестирования"),
            SkillsOrm(name="UX/UI"),
            SkillsOrm(name="HTML"),
            SkillsOrm(name="CSS"),
            SkillsOrm(name="React"),
            SkillsOrm(name="Angular"),
            SkillsOrm(name="Vue"),
            SkillsOrm(name="Node.js"),
            SkillsOrm(name="Express.js"),
            SkillsOrm(name="RESTful API"),
            SkillsOrm(name="GraphQL"),
            SkillsOrm(name="ООП"),
            SkillsOrm(name="Функциональное программирование"),
            SkillsOrm(name="Паттерны"),
            SkillsOrm(name="Алгоритмы"),
            SkillsOrm(name="Безопасность"),
            SkillsOrm(name="Шифрование"),
            SkillsOrm(name="Git"),
            SkillsOrm(name="Agile"),
            SkillsOrm(name="Scrum"),
            SkillsOrm(name="DevOps"),
            SkillsOrm(name="IaC"),
            SkillsOrm(name="Мониторинг"),
            SkillsOrm(name="Системы контроля версий"),
            SkillsOrm(name="Микросервисы"),
            SkillsOrm(name="Сетевое администрирование"),
            SkillsOrm(name="Серверы"),
            SkillsOrm(name="Виртуализация"),
            SkillsOrm(name="Linux"),
            SkillsOrm(name="Windows"),
            SkillsOrm(name="Системное администрирование"),
            SkillsOrm(name="API интеграция"),
            SkillsOrm(name="Чат-боты"),
            SkillsOrm(name="МЛ"),
            SkillsOrm(name="Искусственный интеллект"),
            SkillsOrm(name="Анализ данных"),
            SkillsOrm(name="Визуализация"),
            SkillsOrm(name="Big Data"),
            SkillsOrm(name="Pandas"),
            SkillsOrm(name="TensorFlow"),
            SkillsOrm(name="PyTorch"),
            SkillsOrm(name="CMS"),
            SkillsOrm(name="SEO"),
            SkillsOrm(name="Контент-маркетинг"),
            SkillsOrm(name="Анализ требований"),
            SkillsOrm(name="Архитектура"),
            SkillsOrm(name="Jira"),
            SkillsOrm(name="Поддержка"),
            SkillsOrm(name="Обучение"),
            SkillsOrm(name="Документация"),
            SkillsOrm(name="Обслуживание ПО"),
            SkillsOrm(name="Модули"),
            SkillsOrm(name="Плагины"),
            SkillsOrm(name="REST"),
            SkillsOrm(name="Оптимизация"),
            SkillsOrm(name="Графика"),
            SkillsOrm(name="Обработка изображений"),
            SkillsOrm(name="Интерфейсы"),
            SkillsOrm(name="Анимация"),
            SkillsOrm(name="Соцсети API"),
            SkillsOrm(name="Flutter"),
            SkillsOrm(name="ORM"),
            SkillsOrm(name="Фреймворки"),
            SkillsOrm(name="Методологии"),
            SkillsOrm(name="Код-ревью"),
            SkillsOrm(name="Тестирование"),
            SkillsOrm(name="Окружения"),
            SkillsOrm(name="FinTech"),
            SkillsOrm(name="eCommerce"),
            SkillsOrm(name="Управление проектами"),
            SkillsOrm(name="Протоколы"),
            SkillsOrm(name="UX"),
            SkillsOrm(name="SVN"),
            SkillsOrm(name="Внедрение"),
            SkillsOrm(name="Тренинги"),
            SkillsOrm(name="Конфигурация"),
            SkillsOrm(name="Анализ кода"),
            SkillsOrm(name="Карты API"),
            SkillsOrm(name="Open-source")
        ]
        session.add_all(skills)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(recreate())
    asyncio.run(add_skills())
