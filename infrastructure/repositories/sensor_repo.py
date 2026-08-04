from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import Sensor

class SensorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
