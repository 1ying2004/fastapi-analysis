"""
贡献者可视化模块

生成贡献者相关图表
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()


def plot_contributions_distribution(contributors, output_dir='output'):
    """贡献分布直方图"""
    os.makedirs(output_dir, exist_ok=True)
    
    contributions = [c['contributions'] for c in contributors]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    bins = [1, 5, 10, 50, 100, 500, 1000, 5000, 10000]
    n, bins_out, patches = ax.hist(contributions, bins=bins, color='#9f7aea', 
                                    edgecolor='white', alpha=0.8)
    
    for i, patch in enumerate(patches):
        height = patch.get_height()
        if height > 0:
            ax.text(patch.get_x() + patch.get_width()/2, height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    ax.set_xscale('log')
    ax.set_xlabel('贡献数（对数刻度）', fontsize=14, fontweight='bold')
    ax.set_ylabel('贡献者数量', fontsize=14, fontweight='bold')
    ax.set_title('贡献分布', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/contributions_dist.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 贡献分布: {output_dir}/contributions_dist.png")


def plot_top_contributors(contributors, output_dir='output', top_n=20):
    """Top贡献者柱状图"""
    os.makedirs(output_dir, exist_ok=True)
    
    top = sorted(contributors, key=lambda x: -x['contributions'])[:top_n]
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    names = [c['login'] for c in top]
    values = [c['contributions'] for c in top]
    colors = plt.cm.Purples(np.linspace(0.4, 0.9, len(top)))[::-1]
    
    bars = ax.barh(range(len(top)), values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + max(values)*0.01, bar.get_y() + bar.get_height()/2,
               f'{int(width):,}', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('贡献数 (GitHub API统计)', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} GitHub贡献者排行 (按GitHub贡献数)', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_contributors.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Top贡献者: {output_dir}/top_contributors.png")


def plot_contribution_pie(contributors, output_dir='output'):
    """贡献占比饼图"""
    os.makedirs(output_dir, exist_ok=True)
    
    sorted_c = sorted(contributors, key=lambda x: -x['contributions'])
    top10 = sorted_c[:10]
    others = sorted_c[10:]
    
    labels = [c['login'] for c in top10]
    values = [c['contributions'] for c in top10]
    
    if others:
        labels.append('其他')
        values.append(sum(c['contributions'] for c in others))
    
    fig, ax = plt.subplots(figsize=(12, 10))
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%',
        colors=colors, startangle=90, explode=[0.02]*len(labels)
    )
    
    ax.set_title('贡献占比', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/contribution_pie.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 贡献占比: {output_dir}/contribution_pie.png")
