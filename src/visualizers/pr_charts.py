"""
PR可视化模块

生成Pull Requests相关图表
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()


def plot_pr_state(prs, output_dir='output'):
    """PR状态分布饼图"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not prs:
        return
    
    states = {}
    for pr in prs:
        state = pr.get('state', 'unknown')
        states[state] = states.get(state, 0) + 1
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#48bb78', '#f56565', '#667eea']
    
    labels = ['已合并/关闭' if s == 'closed' else '开放' for s in states.keys()]
    
    wedges, texts, autotexts = ax.pie(
        states.values(),
        labels=labels,
        autopct='%1.1f%%',
        colors=colors[:len(states)],
        explode=[0.02] * len(states),
        shadow=True
    )
    
    ax.set_title('PR状态分布', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/pr_state.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ PR状态图: {output_dir}/pr_state.png")


def plot_pr_timeline(prs, output_dir='output'):
    """PR创建时间线"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not prs:
        return
    
    df = pd.DataFrame(prs)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    df = df.dropna(subset=['created_at'])
    df['month'] = df['created_at'].dt.to_period('M')
    
    monthly = df.groupby('month').size()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    x = range(len(monthly))
    ax.fill_between(x, monthly.values, alpha=0.3, color='#9f7aea')
    ax.plot(x, monthly.values, linewidth=2, color='#9f7aea', marker='o', markersize=3)
    
    step = max(1, len(monthly) // 15)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([str(m) for m in monthly.index[::step]], rotation=45, ha='right')
    
    ax.set_xlabel('月份', fontsize=14, fontweight='bold')
    ax.set_ylabel('新增PR数', fontsize=14, fontweight='bold')
    ax.set_title('PR创建时间线', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/pr_timeline.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ PR时间线: {output_dir}/pr_timeline.png")


def plot_top_pr_authors(prs, output_dir='output', top_n=15):
    """Top PR创建者"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not prs:
        return
    
    from collections import Counter
    authors = Counter(pr['author'] for pr in prs)
    top = authors.most_common(top_n)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = plt.cm.Purples(np.linspace(0.4, 0.9, len(top)))[::-1]
    
    names = [t[0] for t in top]
    counts = [t[1] for t in top]
    
    bars = ax.barh(range(len(top)), counts, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
               f'{int(width)}', va='center', fontsize=10)
    
    ax.set_xlabel('PR数', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} PR贡献者', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_pr_authors.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Top PR贡献者: {output_dir}/top_pr_authors.png")
