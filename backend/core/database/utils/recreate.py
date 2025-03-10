import asyncio

from backend.core.database.settings.database import engine, Base, session_factory
from backend.core.database.models.other.Skill import SkillsOrm
from backend.core.database.models.other.Profession import ProfessionsOrm


async def recreate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_skills():
    async with session_factory() as session:
        skills = [
            "Python",
            "Java",
            "C#",
            "JavaScript",
            "Ruby",
            "PHP",
            "Go",
            "Rust",
            "C++",
            "Веб-разработка",
            "Мобильная разработка",
            "API",
            "Игровая разработка",
            "SQL",
            "NoSQL",
            "Оптимизация БД",
            "Администрирование БД",
            "Docker",
            "Kubernetes",
            "Облачные вычисления",
            "CI/CD",
            "Автоматизация тестирования",
            "UX/UI",
            "HTML",
            "CSS",
            "React",
            "Angular",
            "Vue",
            "Node.js",
            "Express.js",
            "RESTful API",
            "GraphQL",
            "ООП",
            "Функциональное программирование",
            "Паттерны",
            "Алгоритмы",
            "Безопасность",
            "Шифрование",
            "Git",
            "Agile",
            "Scrum",
            "DevOps",
            "IaC",
            "Мониторинг",
            "Системы контроля версий",
            "Микросервисы",
            "Сетевое администрирование",
            "Серверы",
            "Виртуализация",
            "Linux",
            "Windows",
            "Системное администрирование",
            "API интеграция",
            "Чат-боты",
            "МЛ",
            "Искусственный интеллект",
            "Анализ данных",
            "Визуализация",
            "Big Data",
            "Pandas",
            "TensorFlow",
            "PyTorch",
            "CMS",
            "SEO",
            "Контент-маркетинг",
            "Анализ требований",
            "Архитектура",
            "Jira",
            "Поддержка",
            "Обучение",
            "Документация",
            "Обслуживание ПО",
            "Модули",
            "Плагины",
            "REST",
            "Оптимизация",
            "Графика",
            "Обработка изображений",
            "Интерфейсы",
            "Анимация",
            "Соцсети API",
            "Flutter",
            "ORM",
            "Фреймворки",
            "Методологии",
            "Код-ревью",
            "Тестирование",
            "Окружения",
            "FinTech",
            "eCommerce",
            "Управление проектами",
            "Протоколы",
            "UX",
            "SVN",
            "Внедрение",
            "Тренинги",
            "Конфигурация",
            "Анализ кода",
            "Карты API",
            "Open-source"
        ]
        skills_orm = [SkillsOrm(name=skill) for skill in skills]
        session.add_all(skills_orm)
        await session.commit()


async def add_professions():
    async with session_factory() as session:
        professions = [
            "Программист",
            "Веб-разработчик",
            "Мобильный разработчик",
            "Системный администратор",
            "Специалист по кибербезопасности",
            "Аналитик данных",
            "Data Scientist",
            "DevOps-инженер",
            "QA-инженер (тестировщик)",
            "Архитектор программного обеспечения",
            "IT-менеджер",
            "Сетевой администратор",
            "Бизнес-аналитик",
            "Специалист по машинному обучению",
            "UX/UI-дизайнер",
            "Инженер по облачным технологиям",
            "Блокчейн-разработчик",
            "Специалист по виртуализации",
            "Инженер по базам данных",
            "Системный аналитик",
            "Разработчик игр",
            "Специалист по автоматизации тестирования",
            "Администратор баз данных",
            "Специалист по интеграции систем",
            "Инженер по технической поддержке",
            "Разработчик интерфейсов",
            "Специалист по SEO",
            "Технический писатель",
            "Специалист по интернет-маркетингу",
            "Программист на Python",
            "Программист на Java",
            "Программист на C#",
            "Программист на JavaScript",
            "Специалист по API",
            "Инженер по системной архитектуре",
            "Специалист по аналитике веб-трафика",
            "Разработчик программного обеспечения",
            "Специалист по виртуальной реальности",
            "Специалист по дополненной реальности",
            "Инженер по робототехнике"
        ]
        professions_orm = [ProfessionsOrm(title=profession) for profession in professions]
        session.add_all(professions_orm)
        await session.commit()


if __name__ == '__main__':
    asyncio.run(recreate())
    asyncio.run(add_skills())
    asyncio.run(add_professions())
