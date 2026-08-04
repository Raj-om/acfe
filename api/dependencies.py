from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.connection import get_db

async def get_db_session(session: AsyncSession = Depends(get_db)):
    return session
