from fastapi import FastAPI
from app.api.v1 import registry, conversion, validation, lookups, adapter
from app.core.config import settings

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

# Include Routers
app.include_router(registry.router, prefix="/api/v1", tags=["Registry"])
app.include_router(conversion.router, prefix="/api/v1/convert", tags=["Utilities"])
app.include_router(validation.router, prefix="/api/v1/validate", tags=["Utilities"])
app.include_router(lookups.router, prefix="/api/v1/lookup", tags=["Utilities"])
app.include_router(adapter.router, prefix="/api/v1/adapter", tags=["Web Adapter"])

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to AgentHub. Refer to /docs or /api/v1/registry for agent-readable schemas."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
