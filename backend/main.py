import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="maritime-career API", version="0.1.0")
logger = logging.getLogger("api")


@app.get("/health")
async def health():
    logger.info("health check")
    return JSONResponse({"status": "ok"})


@app.get("/api/v1/jobs")
async def list_jobs():
    logger.info("list jobs called")
    return JSONResponse({"jobs": []})
