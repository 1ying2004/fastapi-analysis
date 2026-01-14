"""
依赖可视化模块

生成依赖相关图表
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()


def plot_import_frequency(dependency_data, output_dir='output', top_n=20):
    """
    绘制模块导入频率图
    
    Args:
        dependency_data: 依赖分析数据
        output_dir: 输出目录
        top_n: 显示前N个
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not dependency_data:
        return
    
    from collections import Counter
    all_imports = []
    for deps in dependency_data.values():
        all_imports.extend(deps)
    
    counts = Counter(all_imports).most_common(top_n)
    
    if not counts:
        return
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    labels = [c[0] for c in counts]
    values = [c[1] for c in counts]
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(counts)))[::-1]
    
    bars = ax.barh(range(len(counts)), values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
               f'{int(width)}', va='center', fontsize=10)
    
    ax.set_xlabel('被导入次数', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} 高频导入模块', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/import_frequency.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 导入频率图: {output_dir}/import_frequency.png")


def plot_file_dependencies(dependency_data, output_dir='output', top_n=15):
    """
    绘制文件依赖数量图
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not dependency_data:
        return
    
    file_deps = [(f, len(deps)) for f, deps in dependency_data.items()]
    file_deps.sort(key=lambda x: -x[1])
    top = file_deps[:top_n]
    
    if not top:
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    labels = [os.path.basename(f[0]) for f in top]
    values = [f[1] for f in top]
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top)))[::-1]
    
    bars = ax.barh(range(len(top)), values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.2, bar.get_y() + bar.get_height()/2,
               f'{int(width)}', va='center', fontsize=10)
    
    ax.set_xlabel('依赖模块数', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} 依赖最多的文件', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/file_dependencies.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 文件依赖图: {output_dir}/file_dependencies.png")
