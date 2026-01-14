"""
文件统计可视化
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_file_types(file_stats, output_dir='output'):
    """绘制文件类型分布 - 水平柱状图"""
    os.makedirs(output_dir, exist_ok=True)
    
    sorted_stats = sorted(file_stats.items(), key=lambda x: -x[1])[:15]
    
    if not sorted_stats:
        return
    
    labels = [s[0] if s[0] else '无扩展名' for s in sorted_stats]
    values = [s[1] for s in sorted_stats]
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(labels)))
    bars = ax.barh(range(len(labels)), values, color=colors, edgecolor='white', height=0.7)
    
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=12)
    ax.invert_yaxis()
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        pct = width / sum(values) * 100
        ax.text(width + max(values)*0.01, bar.get_y() + bar.get_height()/2,
               f'{int(width):,} ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('文件数量', fontsize=14, fontweight='bold')
    ax.set_title('文件类型分布', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    total = sum(values)
    ax.text(0.95, 0.02, f'总计: {total:,} 个文件', transform=ax.transAxes,
           fontsize=12, ha='right', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/file_types.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 文件类型: {output_dir}/file_types.png")

def plot_loc_bar(loc_data, output_dir='output'):
    """绘制代码行数柱状图"""
    os.makedirs(output_dir, exist_ok=True)
    
    categories = ['代码行', '空行', '注释行']
    values = [loc_data.get('code', 0), loc_data.get('blank', 0), loc_data.get('comment', 0)]
    colors = ['#667eea', '#a0aec0', '#48bb78']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2, width=0.6)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + max(values)*0.02,
               f'{int(height):,}', ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('行数', fontsize=14, fontweight='bold')
    ax.set_title('代码行数统计', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    total = sum(values)
    ax.text(0.95, 0.95, f'总计: {total:,} 行', transform=ax.transAxes,
           fontsize=14, fontweight='bold', ha='right', va='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/loc_bar.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 代码行数: {output_dir}/loc_bar.png")
