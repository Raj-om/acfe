from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from .routers import fusion, sensors, alerts, explain, health, admin
from .middleware import LogMiddleware, RateLimitMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title="ACFE API",
    description="Adaptive Confidence Fusion Engine API",
    version="1.0.0",
    contact={"name": "Engineering Team"},
    license_info={"name": "Proprietary"},
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(LogMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(fusion.router, prefix="/api/v1/fuse")
app.include_router(sensors.router, prefix="/api/v1/sensors")
app.include_router(alerts.router, prefix="/api/v1/alerts")
app.include_router(explain.router, prefix="/api/v1/explain")
app.include_router(health.router)
app.include_router(admin.router, prefix="/api/v1/admin")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
