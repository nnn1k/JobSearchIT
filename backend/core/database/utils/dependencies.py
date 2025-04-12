from backend.core.database.database import session_factory


async def get_db():
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
            print('commit')
        except Exception as e:
            await session.rollback()
            print(f'Rollback due to: {str(e)}')
            raise e
        finally:
            await session.close()
