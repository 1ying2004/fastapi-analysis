"""
装饰器
"""
import time
from functools import wraps
from src.utils.logger import logger

def timer(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} 耗时: {elapsed:.2f}秒")
        return result
    return wrapper

def retry(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:
                        raise
                    logger.warning(f"{func.__name__} 重试 {i+1}/{max_retries}")
                    time.sleep(delay)
        return wrapper
    return decorator

def catch_errors(default=None):
    """异常捕获装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"{func.__name__} 错误: {e}")
                return default
        return wrapper
    return decorator
