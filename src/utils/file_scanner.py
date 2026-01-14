"""
文件扫描器 - 扫描项目中的Python文件
"""
import os
from typing import List, Generator

def find_python_files(path: str) -> Generator[str, None, None]:
    """查找所有Python文件"""
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)

def get_project_files(path: str) -> List[str]:
    """获取项目文件列表"""
    return list(find_python_files(path))

def count_files_by_extension(path: str) -> dict:
    """按扩展名统计文件数"""
    counts = {}
    for root, _, files in os.walk(path):
        for f in files:
            ext = os.path.splitext(f)[1] or 'no_ext'
            counts[ext] = counts.get(ext, 0) + 1
    return counts
