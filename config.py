import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


ROOT_DIR = Path(__file__)
LOG_DIR = 'logs'


@dataclass
class BaseConfig:
    BOT_TOKEN: str
    OPENWEATHER_API_KEY: str
    OPENWEATHER_API_URL: str


def load_config():
    # Logger Config
    logger.add(Path(ROOT_DIR.parent, LOG_DIR, 'info.log'),
               rotation='1 day',
               retention='14 days',
               level='INFO',
               enqueue=True)

    load_dotenv()
    config = BaseConfig(
        BOT_TOKEN=os.getenv('BOT_TOKEN'),
        OPENWEATHER_API_KEY=os.getenv('OPENWEATHER_API_KEY'),
        OPENWEATHER_API_URL=os.getenv('OPENWEATHER_API_URL'),
    )

    logger.info('Configuration Loaded')
    return config


base_config = load_config()
