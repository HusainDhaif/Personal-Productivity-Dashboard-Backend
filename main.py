import logging
import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from controllers.users import router as users_router
from app.routes.tasks import router as tasks_router
from app.routes.habits import router as habits_router
from app.routes.notes import router as notes_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Personal Productivity Dashboard API",
    description="Backend API for Personal Productivity Dashboard",
    version="1.0.0"
)

load_dotenv()
current_environment = os.getenv("ENVIRONMENT", "development")

if current_environment == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    client_host = request.client.host if request.client else 'unknown'
    logger.info(f"Incoming request: {request.method} {request.url.path} from {client_host}")
    
    try:
        response = await call_next(request)
        elapsed_time = time.time() - start_time
        
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {elapsed_time:.3f}s"
        )
        
        return response
    except Exception as error:
        elapsed_time = time.time() - start_time
        logger.error(
            f"Error processing {request.method} {request.url.path}: {str(error)} "
            f"Time: {elapsed_time:.3f}s",
            exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(habits_router)
app.include_router(notes_router)

@app.get("/")
def read_root():
    return {"message": "Personal Productivity Dashboard API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Personal Productivity Dashboard API"}