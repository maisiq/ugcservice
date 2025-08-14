from motor.motor_asyncio import AsyncIOMotorClientSession
from src.logger.logger import get_logger


class MongoUOW:
    def __init__(self, session: AsyncIOMotorClientSession) -> None:
        self._session = session
        self._logger = get_logger()

    async def __aenter__(self):
        self._session.start_transaction()
        return self

    async def __aexit__(self, exc_type, exc: Exception, tb):
        if self._session.in_transaction:
            await self.rollback()

    async def commit(self):
        if not self._session.in_transaction:
            raise RuntimeError('No active transaction to commit')
        self._logger.debug('Commiting MongoDB transaction with session_id data: %s', self._session.session_id)
        await self._session.commit_transaction()

    async def rollback(self):
        self._logger.debug('Rollback MongoDB transaction with session_id data: %s', self._session.session_id)
        await self._session.abort_transaction()
