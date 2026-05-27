"""Configuração de logging para o projeto SkyData"""

import logging
import sys
from pathlib import Path

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

logger = logging.getLogger('skydata')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_DIR / 'skydata.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger(name):
    return logging.getLogger(f'skydata.{name}')
