from fastapi import FastAPI
from app.api.v1 import auth, properties, clients, deals, stats

app = FastAPI(title="Real Estate SaaS", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(properties.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(deals.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok", "message": "النظام يعمل"}