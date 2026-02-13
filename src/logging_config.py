# src/logging_config.py

from logging.handlers import RotatingFileHandler
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

def setup_logging():

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(file_handler)
    root.addHandler(console_handler)
    
setup_logging()

def main():
    logger = logging.getLogger(__name__)

    logger.info("testing")
if __name__ == "__main__":
    main()
# print(f"BASE_DIR: {BASE_DIR}")
# print(f"LOG_DIR : {LOG_DIR}")
# print(f"LOG_FILE : {LOG_FILE}")