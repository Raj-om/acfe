import pytest
import pytest_asyncio
from httpx import AsyncClient
# Assuming main app import will be available later
# from acfe.main import app 

@pytest_asyncio.fixture
async def test_client():
    # async with AsyncClient(app=app, base_url="http://test") as client:
    #     yield client
    pass

@pytest.fixture
def test_database():
    # Setup test DB
    yield
    # Teardown

@pytest.fixture
def mock_sensors():
    return [
        {"id": "sensor_1", "confidence": 0.9, "value": 1.0},
        {"id": "sensor_2", "confidence": 0.8, "value": 1.2},
        {"id": "sensor_3", "confidence": 0.4, "value": 0.5},
    ]

@pytest.fixture
def sample_fusion_request(mock_sensors):
    return {
        "sensors": mock_sensors,
        "timestamp": "2026-08-03T19:00:00Z"
    }
