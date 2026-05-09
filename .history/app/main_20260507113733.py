from fastapi import FastAPI

app = FastAPI(title="Real Estate SaaS", version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "ok", "message": "النظام يعمل"}