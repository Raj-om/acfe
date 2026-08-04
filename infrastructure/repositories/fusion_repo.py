from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import FusionResult

class FusionResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
