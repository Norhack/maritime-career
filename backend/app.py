from fastapi import FastAPI
from backend.api.intelligence import router as intelligence_router
from backend.services.intelligence_scheduler import IntelligenceScheduler

app = FastAPI(title="Maritime Career Intelligence API")
app.include_router(intelligence_router)

scheduler = IntelligenceScheduler()

@app.on_event("startup")
def startup_event():
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.stop()

@app.get("/health")
def health():
    return {"status": "ok"}
