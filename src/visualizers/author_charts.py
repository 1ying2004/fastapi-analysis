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
    """绘制top作者柱状图"""
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
    
    ax.set_xlabel('提交数', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} 贡献者', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_authors.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Top作者: {output_dir}/top_authors.png")
