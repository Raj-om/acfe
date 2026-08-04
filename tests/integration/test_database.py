import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, String, Float, Integer, Boolean
from uuid import uuid4

# Dummy Base and Models for testing
Base = declarative_base()

class SensorModel(Base):
    __tablename__ = 'sensors'
    id = Column(String, primary_key=True)
    name = Column(String)
    reliability = Column(Float, default=1.0)
    
class FusionResultModel(Base):
    __tablename__ = 'fusion_results'
    id = Column(String, primary_key=True)
    session_id = Column(String, index=True)
    confidence = Column(Float)
    
class AlertModel(Base):
    __tablename__ = 'alerts'
    id = Column(String, primary_key=True)
    severity = Column(String)
    acknowledged = Column(Boolean, default=False)

@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session(engine):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_create_and_retrieve_sensor(db_session):
    """Test: create sensor -> retrieve sensor by ID"""
    sensor_id = str(uuid4())
    sensor = SensorModel(id=sensor_id, name="Test Sensor", reliability=0.9)
    
    db_session.add(sensor)
    await db_session.commit()
    
    retrieved = await db_session.get(SensorModel, sensor_id)
    assert retrieved is not None
    assert retrieved.name == "Test Sensor"
    assert retrieved.reliability == 0.9

@pytest.mark.asyncio
async def test_create_fusion_result_retrieve_by_session(db_session):
    """Test: create fusion result -> retrieve by session_id"""
    session_id = "session_123"
    result_id = str(uuid4())
    result = FusionResultModel(id=result_id, session_id=session_id, confidence=0.85)
    
    db_session.add(result)
    await db_session.commit()
    
    from sqlalchemy import select
    stmt = select(FusionResultModel).where(FusionResultModel.session_id == session_id)
    results = (await db_session.execute(stmt)).scalars().all()
    
    assert len(results) == 1
    assert results[0].confidence == 0.85

@pytest.mark.asyncio
async def test_create_list_acknowledge_alert(db_session):
    """Test: create alert -> list alerts -> acknowledge alert"""
    alert_id = str(uuid4())
    alert = AlertModel(id=alert_id, severity="HIGH", acknowledged=False)
    db_session.add(alert)
    await db_session.commit()
    
    from sqlalchemy import select
    # List unacknowledged
    stmt = select(AlertModel).where(AlertModel.acknowledged == False)
    alerts = (await db_session.execute(stmt)).scalars().all()
    assert len(alerts) == 1
    
    # Acknowledge
    alert_to_ack = alerts[0]
    alert_to_ack.acknowledged = True
    await db_session.commit()
    
    # Verify acknowledged
    stmt = select(AlertModel).where(AlertModel.acknowledged == False)
    alerts = (await db_session.execute(stmt)).scalars().all()
    assert len(alerts) == 0

@pytest.mark.asyncio
async def test_pagination(db_session):
    """Test: pagination works (limit, offset)"""
    for i in range(15):
        db_session.add(SensorModel(id=str(uuid4()), name=f"Sensor {i}"))
    await db_session.commit()
    
    from sqlalchemy import select
    stmt = select(SensorModel).order_by(SensorModel.name).limit(5).offset(5)
    results = (await db_session.execute(stmt)).scalars().all()
    
    assert len(results) == 5

@pytest.mark.asyncio
async def test_sensor_not_found(db_session):
    """Test: sensor not found -> returns None"""
    retrieved = await db_session.get(SensorModel, "non_existent_id")
    assert retrieved is None

@pytest.mark.asyncio
async def test_duplicate_sensor_id(db_session):
    """Test: duplicate sensor ID -> raises IntegrityError"""
    sensor_id = str(uuid4())
    sensor1 = SensorModel(id=sensor_id, name="S1")
    sensor2 = SensorModel(id=sensor_id, name="S2")
    
    db_session.add(sensor1)
    await db_session.commit()
    
    db_session.add(sensor2)
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError):
        await db_session.commit()
