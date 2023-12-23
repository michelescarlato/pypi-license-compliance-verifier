import logging
import time
from pathlib import Path


Path("logs").mkdir(parents=True, exist_ok=True)
formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
time_string = time.strftime("%Y%m%d-%H%M%S")
file_handler = logging.FileHandler(f'logs/pypi_lcv_{time_string}.log', mode='w')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
