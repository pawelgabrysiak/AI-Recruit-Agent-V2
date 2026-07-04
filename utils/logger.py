import logging
import os
from pathlib import Path
from utils.config import config

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # File handler
    log_path_str = config.get("paths", {}).get("log_file", "output/app.log")
    log_path = Path(log_path_str)
    
    # Ensure directory exists
    os.makedirs(log_path.parent, exist_ok=True)
    
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(file_handler)
    
    return logger
