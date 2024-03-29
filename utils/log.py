import logging
import os

logging.config.fileConfig(f'{os.getcwd()}/app/logging.conf', disable_existing_loggers=True)
logger = logging.getLogger(__name__)