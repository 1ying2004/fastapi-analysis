"""
代码重复检测模块

检测项目中的重复代码块
"""
import os
import hashlib
from collections import defaultdict


def hash_code_block(lines, min_lines=5):
    """
    对代码块进行哈希
    
    Args:
        lines: 代码行列表
        min_lines: 最小行数阈值
    
    Returns:
        哈希值或None
    """
    if len(lines) < min_lines:
        return None
    
    normalized = '\n'.join(line.strip() for line in lines if line.strip())
    return hashlib.md5(normalized.encode()).hexdigest()


def find_duplicates(project_path, block_size=10):
    """
    查找重复代码块
    
    Args:
        project_path: 项目路径
        block_size: 检测的代码块大小
    
    Returns:
        重复代码块信息
    """
    blocks = defaultdict(list)
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for f in files:
            if not f.endswith('.py'):
                continue
            
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except:
                continue
            
            for i in range(len(lines) - block_size + 1):
                block = lines[i:i + block_size]
                block_hash = hash_code_block(block)
                
                if block_hash:
                    blocks[block_hash].append({
                        'file': filepath,
                        'start_line': i + 1,
                        'end_line': i + block_size
                    })
    
    duplicates = {k: v for k, v in blocks.items() if len(v) > 1}
    return duplicates


def get_duplication_stats(project_path):
    """获取重复统计"""
    duplicates = find_duplicates(project_path)
    
    total_duplicates = sum(len(v) for v in duplicates.values())
    unique_patterns = len(duplicates)
    
    return {
        'unique_duplicate_patterns': unique_patterns,
        'total_duplicate_blocks': total_duplicates,
        'duplication_ratio': total_duplicates / max(1, unique_patterns)
    }
