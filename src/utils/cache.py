"""
缓存模块 - 避免重复请求
"""
import json
import os
import hashlib
from datetime import datetime, timedelta

CACHE_DIR = 'cache'
CACHE_EXPIRE_HOURS = 24

def _ensure_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def _get_cache_path(key):
    hash_key = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hash_key}.json")

def save_cache(key, data):
    """保存缓存"""
    _ensure_dir()
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    with open(_get_cache_path(key), 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, ensure_ascii=False)

def load_cache(key, max_age_hours=CACHE_EXPIRE_HOURS):
    """加载缓存（带过期检查）"""
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
    """清空缓存"""
    if os.path.exists(CACHE_DIR):
        for f in os.listdir(CACHE_DIR):
            os.remove(os.path.join(CACHE_DIR, f))
        print("缓存已清空")
