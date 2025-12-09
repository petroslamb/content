import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """
    Configure a standardized logger for the ingestion pipeline.
    
    Features:
    - Console Handler: INFO level, minimal formatting.
    - File Handler: DEBUG level, detailed timestamped formatting.
    - File Path: research_artifacts/scorecard_dataset/logs/pipeline.log
    - Rotation: 10MB per file, keep 3 backups.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture everything at source

    # meaningful idempotent setup
    if logger.hasHandlers():
        return logger

    # Ensure log directory exists
    base_dir = Path(__file__).resolve().parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "pipeline.log"

    # 1. File Handler (Detailed history)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=3)
    file_handler.setLevel(logging.INFO)  # Keep logs clean (INFO), use DEBUG only if needed
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 2. Console Handler (User feedback)
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING) # Console is for errors only
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
