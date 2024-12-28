import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from contextlib import asynccontextmanager
from config.logger import logger
from config.database import db_instance
from config.scheduler import CallPlanScheduler
from routes import auth_router, lead_router
from utils.environments import SERVER_PORT, SERVER_HOST
from models import Base, KeyAccountManager, Lead, LeadCallPlan, Contact, CallRecord

# Store scheduler instance
scheduler_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application startup and shutdown events."""
    # Startup
    global scheduler_instance
    scheduler_instance = CallPlanScheduler()
    scheduler_instance.start()
    
    yield  # Server is running and handling requests

    # Shutdown
    if scheduler_instance:
        scheduler_instance.stop()

app = FastAPI(lifespan=lifespan)

# Global exception handler middleware
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    else:
        logger.error("Internal server error: %s", str(exc), stack_info=True)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

app.include_router(auth_router, prefix="/api/v1")
app.include_router(lead_router, prefix="/api/v1")

@app.get("/api/v1/check")
async def root():
    return {"message": "Okay"}

if __name__ == "__main__":
    Base.metadata.create_all(bind=db_instance.engine)
    uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)