"""
日志模块

提供统一的日志记录功能。
"""
import logging
import os
from datetime import datetime

LOG_DIR = 'logs'


def setup_logger(name='fastapi_analysis', level=logging.INFO):
    """
    配置并返回logger实例
    
    Args:
        name: logger名称
        level: 日志级别
    
    Returns:
        配置好的logger实例
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if logger.handlers:
        return logger
    
    log_file = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()
