"""
代码复杂度可视化
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()


def plot_complexity_distribution(analysis_results, output_dir='output'):
    """复杂度分布图 - 美化版"""
    os.makedirs(output_dir, exist_ok=True)
    
    complexities = []
    for file_result in analysis_results.get('files', []):
        for func in file_result.get('functions', []):
            complexities.append(func.get('complexity', 1))
    
    if not complexities:
        print("  无复杂度数据")
        return
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    max_comp = min(max(complexities), 15)
    bins = list(range(1, max_comp + 2))
    
    n, bins_out, patches = ax.hist(complexities, bins=bins, color='#667eea', 
                                    edgecolor='white', alpha=0.8, rwidth=0.85)
    
    for rect in patches:
        height = rect.get_height()
        if height > 0:
            ax.text(rect.get_x() + rect.get_width()/2, height + 20,
                   f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('圈复杂度', fontsize=14, fontweight='bold')
    ax.set_ylabel('函数数量', fontsize=14, fontweight='bold')
    ax.set_title('函数圈复杂度分布', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    ax.set_xticks(range(1, max_comp + 1))
    
    avg = np.mean(complexities)
    ax.axvline(avg, color='#f56565', linestyle='--', linewidth=2)
    ax.text(avg + 0.2, ax.get_ylim()[1] * 0.9, f'平均: {avg:.2f}', 
           fontsize=12, color='#f56565', fontweight='bold')
    
    low = len([c for c in complexities if c <= 3])
    med = len([c for c in complexities if 4 <= c <= 7])
    high = len([c for c in complexities if c > 7])
    
    info_text = f'低(1-3): {low}\n中(4-7): {med}\n高(>7): {high}'
    ax.text(0.95, 0.95, info_text, transform=ax.transAxes,
           fontsize=11, ha='right', va='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
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
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    names = [f[0][:30] for f in top]
    counts = [f[1] for f in top]
    colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(top)))
    
    bars = ax.barh(range(len(top)), counts, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
               f'{int(width)}', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('函数数量', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} 文件函数数量', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/function_count.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 函数数量: {output_dir}/function_count.png")
