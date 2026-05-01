from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger
from api.routes import router
from config.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("RepoPilot starting up...")
    yield
    logger.info("RepoPilot shutting down.")

app = FastAPI(
    title="RepoPilot",
    description="AI-powered codebase understanding assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    from config.settings import settings
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)