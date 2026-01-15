"""
作者统计可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_top_authors(commits, output_dir='output', top_n=15):
    """绘制top作者提交数排行"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    top = df['author'].value_counts().head(top_n)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top)))[::-1]
    bars = ax.barh(range(len(top)), top.values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top.index, fontsize=11)
    ax.invert_yaxis()
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 5, bar.get_y() + bar.get_height()/2,
               f'{int(width):,}', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('提交数量', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} 提交作者排行 (按Git提交数)', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    total = len(commits)
    top_total = top.sum()
    ax.text(0.95, 0.02, f'Top{top_n}共计: {top_total:,} / 总计: {total:,} ({top_total/total*100:.1f}%)',
           transform=ax.transAxes, fontsize=10, ha='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_authors.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Top作者: {output_dir}/top_authors.png")
