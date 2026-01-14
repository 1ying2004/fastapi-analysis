"""
代码复杂度可视化
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_complexity_distribution(analysis_results, output_dir='output'):
    """复杂度分布直方图"""
    os.makedirs(output_dir, exist_ok=True)
    
    complexities = []
    for file_result in analysis_results.get('files', []):
        for func in file_result.get('functions', []):
            complexities.append(func.get('complexity', 1))
    
    if not complexities:
        print("无复杂度数据")
        return
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    bins = range(1, max(complexities) + 2)
    n, bins, patches = ax.hist(complexities, bins=bins, color='#667eea', 
                               edgecolor='white', alpha=0.8, rwidth=0.85)
    
    for i, patch in enumerate(patches):
        if n[i] > 0:
            ax.text(patch.get_x() + patch.get_width()/2, n[i],
                   f'{int(n[i])}', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('圈复杂度', fontsize=14, fontweight='bold')
    ax.set_ylabel('函数数量', fontsize=14, fontweight='bold')
    ax.set_title('函数圈复杂度分布', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    avg = np.mean(complexities)
    ax.axvline(avg, color='red', linestyle='--', linewidth=2, label=f'平均: {avg:.2f}')
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/complexity_dist.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 复杂度分布: {output_dir}/complexity_dist.png")

def plot_function_count_by_file(analysis_results, output_dir='output', top_n=20):
    """文件函数数量排行"""
    os.makedirs(output_dir, exist_ok=True)
    
    file_counts = []
    for file_result in analysis_results.get('files', []):
        filepath = file_result.get('filepath', '')
        filename = os.path.basename(filepath)
        count = file_result.get('total_functions', 0)
        if count > 0:
            file_counts.append((filename, count))
    
    file_counts.sort(key=lambda x: -x[1])
    top = file_counts[:top_n]
    
    if not top:
        return
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    names = [f[0] for f in top]
    counts = [f[1] for f in top]
    colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(top)))
    
    bars = ax.barh(range(len(top)), counts, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    
    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
               f'{int(bar.get_width())}', va='center', fontsize=10)
    
    ax.set_xlabel('函数数量', fontsize=14, fontweight='bold')
    ax.set_title('Top 20 文件函数数量', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/function_count.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 函数数量: {output_dir}/function_count.png")
