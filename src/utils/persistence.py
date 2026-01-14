"""
数据持久化模块

提供数据保存和加载功能，支持多种格式。
"""
import json
import os
import pandas as pd


def save_json(data, filepath):
    """保存为JSON"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"✓ 保存: {filepath}")


def load_json(filepath):
    """加载JSON"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_csv(data, filepath):
    """保存为CSV"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"✓ 保存: {filepath}")


def load_csv(filepath):
    """加载CSV"""
    if not os.path.exists(filepath):
        return None
    return pd.read_csv(filepath).to_dict('records')


def ensure_data_dirs():
    """确保数据目录存在"""
    dirs = ['data', 'cache', 'logs', 'output']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    return True
