from motor.motor_asyncio import AsyncIOMotorClientSession


class MongoUOW:
    def __init__(self, session: AsyncIOMotorClientSession) -> None:
        self._session = session

    async def __aenter__(self):
        self._session.start_transaction()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session.in_transaction:
            await self._session.abort_transaction()

    async def commit(self):
        if not self._session.in_transaction:
            raise RuntimeError('No active transaction to commit')

        await self._session.commit_transaction()

    async def rollback(self):
        await self._session.abort_transaction()
