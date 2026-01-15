"""
配置验证
"""
import os
from src.config import REPO_PATH, DATA_DIR, OUTPUT_DIR

def verify_repo_exists():
    """验证仓库存在"""
    if not os.path.exists(REPO_PATH):
        return False, f"仓库不存在: {REPO_PATH}"
    
    git_dir = os.path.join(REPO_PATH, '.git')
    if not os.path.exists(git_dir):
        return False, f"不是Git仓库: {REPO_PATH}"
    
    return True, "OK"

def ensure_directories():
    """确保目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs('cache', exist_ok=True)
    return True

def check_dependencies():
    """检查依赖"""
    missing = []
    
    try:
        import pandas
    except ImportError:
        missing.append('pandas')
    
    try:
        import matplotlib
    except ImportError:
        missing.append('matplotlib')
    
    try:
        import seaborn
    except ImportError:
        missing.append('seaborn')
    
    if missing:
        return False, f"缺少依赖: {', '.join(missing)}"
    
    return True, "OK"

def run_checks():
    """运行所有检查"""
    results = {}
    
    ok, msg = verify_repo_exists()
    results['repo'] = (ok, msg)
    
    ok, msg = check_dependencies()
    results['deps'] = (ok, msg)
    
    ensure_directories()
    results['dirs'] = (True, "OK")
    
    return results
