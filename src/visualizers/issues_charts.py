"""
Issues可视化模块

生成Issues相关图表
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()


def plot_issues_by_state(issues, output_dir='output'):
    """Issues状态分布饼图"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(issues)
    state_counts = df['state'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#48bb78', '#f56565']
    
    wedges, texts, autotexts = ax.pie(
        state_counts.values,
        labels=['已关闭' if s == 'closed' else '开放' for s in state_counts.index],
        autopct='%1.1f%%',
        colors=colors[:len(state_counts)],
        explode=[0.02] * len(state_counts),
        shadow=True
    )
    
    ax.set_title('Issues状态分布', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/issues_state.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Issues状态图: {output_dir}/issues_state.png")


def plot_issues_timeline(issues, output_dir='output'):
    """Issues创建时间线"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(issues)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)
    df = df.dropna(subset=['created_at'])
    df['month'] = df['created_at'].dt.to_period('M')
    
    monthly = df.groupby('month').size()
    
    fig, ax = plt.subplots(figsize=(16, 6))
    x = range(len(monthly))
    ax.fill_between(x, monthly.values, alpha=0.3, color='#667eea')
    ax.plot(x, monthly.values, linewidth=2, color='#667eea', marker='o', markersize=3)
    
    step = max(1, len(monthly) // 15)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([str(m) for m in monthly.index[::step]], rotation=45, ha='right')
    
    ax.set_xlabel('月份', fontsize=14, fontweight='bold')
    ax.set_ylabel('新增Issues数', fontsize=14, fontweight='bold')
    ax.set_title('Issues创建时间线', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/issues_timeline.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Issues时间线: {output_dir}/issues_timeline.png")


def plot_top_issue_authors(issues, output_dir='output', top_n=15):
    """Top Issue创建者"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(issues)
    top = df['author'].value_counts().head(top_n)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = plt.cm.Oranges(np.linspace(0.4, 0.9, len(top)))[::-1]
    
    bars = ax.barh(range(len(top)), top.values, color=colors, edgecolor='white')
    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top.index, fontsize=10)
    ax.invert_yaxis()
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
               f'{int(width)}', va='center', fontsize=10)
    
    ax.set_xlabel('Issues数', fontsize=14, fontweight='bold')
    ax.set_title(f'Top {top_n} Issue创建者', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_issue_authors.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ Top Issue创建者: {output_dir}/top_issue_authors.png")
