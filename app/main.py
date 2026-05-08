import time
import logging
from fastapi import FastAPI, Depends, Request
from app.api.v1 import registry, conversion, validation, lookups, adapter
from app.core.config import settings
from app.core.auth import verify_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="""
    AgentHub is a middleware platform built for AI agents.
    It provides clean, typed, and versioned data endpoints for common web tasks.

    ### Core Features:
    * **Structured responses** - Every endpoint returns typed JSON.
    * **Agent-readable documentation** - Detailed field descriptions and examples for machine consumption.
    * **Universal utility services** - Currency, unit conversion, validation, and lookups.
    * **Web Adapter** - Proxy layer for human-facing websites.
    * **Schema Registry** - Central directory for service discovery.
    """,
    version=settings.version,
)

# Include Routers with global API Key Auth
app.include_router(
    registry.router,
    prefix="/api/v1",
    tags=["Registry"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    conversion.router,
    prefix="/api/v1/convert",
    tags=["Utilities"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    validation.router,
    prefix="/api/v1/validate",
    tags=["Utilities"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    lookups.router,
    prefix="/api/v1/lookup",
    tags=["Utilities"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    adapter.router,
    prefix="/api/v1/adapter",
    tags=["Web Adapter"],
    dependencies=[Depends(verify_api_key)]
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Path: {request.url.path} Method: {request.method} Time: {process_time:.4f}s")
    return response

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to AgentHub. Refer to /docs or /api/v1/registry for agent-readable schemas."}

@app.get("/health", tags=["Health"])
async def health_check():
    import httpx

    external_services = {
        "frankfurter": "https://api.frankfurter.app/latest",
        "exchangerate_api": "https://api.exchangerate-api.com/v4/latest/USD",
        "timeapi": "https://timeapi.io/api/Time/current/coordinate?latitude=0&longitude=0"
    }

    service_status = {}
    async with httpx.AsyncClient(timeout=2.0) as client:
        for name, url in external_services.items():
            try:
                resp = await client.get(url)
                service_status[name] = "up" if resp.status_code == 200 else "down"
            except httpx.HTTPError:
                service_status[name] = "unreachable"

    return {
        "status": "alive",
        "version": settings.version,
        "app_name": settings.app_name,
        "external_dependencies": service_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
