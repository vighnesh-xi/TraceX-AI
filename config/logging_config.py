import sys
from loguru import logger
from config.settings import settings

def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        colorize=True,
    )
    logger.add(
        "logs/repopilot.log",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
    )