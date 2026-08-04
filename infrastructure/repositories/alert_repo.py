from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import Alert

class AlertRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
