"""
缓存模块

提供文件级缓存功能，支持过期时间控制，
避免重复的API请求和计算。
"""
import json
import os
import hashlib
from datetime import datetime, timedelta

CACHE_DIR = 'cache'
CACHE_EXPIRE_HOURS = 24


def _ensure_dir():
    """确保缓存目录存在"""
    os.makedirs(CACHE_DIR, exist_ok=True)


def _get_cache_path(key):
    """根据key生成缓存文件路径"""
    hash_key = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hash_key}.json")


def save_cache(key, data):
    """
    保存数据到缓存
    
    Args:
        key: 缓存键
        data: 要缓存的数据
    """
    _ensure_dir()
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    with open(_get_cache_path(key), 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False)


def load_cache(key, max_age_hours=CACHE_EXPIRE_HOURS):
    """
    加载缓存数据（带过期检查）
    
    Args:
        key: 缓存键
        max_age_hours: 最大有效时间（小时）
    
    Returns:
        缓存的数据，如果不存在或已过期则返回None
    """
    path = _get_cache_path(key)
    if not os.path.exists(path):
        return None
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        ts = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - ts > timedelta(hours=max_age_hours):
            return None
        
        return cache_data['data']
    except:
        return None


def clear_cache():
    """清空所有缓存"""
    if os.path.exists(CACHE_DIR):
        for f in os.listdir(CACHE_DIR):
            os.remove(os.path.join(CACHE_DIR, f))
        print("✓ 缓存已清空")
