"""
文件统计可视化
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_file_types(file_stats, output_dir='output'):
    """绘制文件类型分布"""
    os.makedirs(output_dir, exist_ok=True)
    
    sorted_stats = sorted(file_stats.items(), key=lambda x: -x[1])[:10]
    
    if not sorted_stats:
        return
    
    labels = [s[0] if s[0] else '无扩展名' for s in sorted_stats]
    values = [s[1] for s in sorted_stats]
    
    fig, ax = plt.subplots(figsize=(12, 10))
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, explode=[0.02] * len(labels),
        textprops={'fontsize': 11}
    )
    
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title('文件类型分布', fontsize=18, fontweight='bold', pad=20)
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
    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 500,
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
