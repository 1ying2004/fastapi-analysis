"""
3D可视化模块

生成3D图表增加视觉效果
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()


def plot_3d_commits_by_year_month(commits, output_dir='output'):
    """3D年月提交分布图"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    pivot = df.groupby(['year', 'month']).size().unstack(fill_value=0)
    
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    years = pivot.index.tolist()
    months = list(range(1, 13))
    
    xpos, ypos, zpos, dx, dy, dz, colors = [], [], [], [], [], [], []
    
    cmap = plt.cm.viridis
    max_val = pivot.values.max()
    
    for i, year in enumerate(years):
        for j, month in enumerate(months):
            val = pivot.loc[year, month] if month in pivot.columns else 0
            xpos.append(i)
            ypos.append(j)
            zpos.append(0)
            dx.append(0.8)
            dy.append(0.8)
            dz.append(val)
            colors.append(cmap(val / max_val))
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, alpha=0.8, edgecolor='white')
    
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years, rotation=45)
    ax.set_yticks(range(12))
    ax.set_yticklabels(['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'])
    
    ax.set_xlabel('年份', fontsize=12, fontweight='bold')
    ax.set_ylabel('月份', fontsize=12, fontweight='bold')
    ax.set_zlabel('提交数', fontsize=12, fontweight='bold')
    ax.set_title('3D 年月提交分布', fontsize=16, fontweight='bold', pad=20)
    
    ax.view_init(elev=25, azim=45)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/commits_3d.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 3D提交图: {output_dir}/commits_3d.png")


def plot_3d_author_activity(commits, output_dir='output', top_n=10):
    """3D作者活跃度图"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    
    top_authors = df['author'].value_counts().head(top_n).index.tolist()
    df_top = df[df['author'].isin(top_authors)]
    
    pivot = df_top.groupby(['author', 'year']).size().unstack(fill_value=0)
    
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    authors = pivot.index.tolist()
    years = pivot.columns.tolist()
    
    xpos, ypos, zpos, dx, dy, dz, colors = [], [], [], [], [], [], []
    cmap = plt.cm.plasma
    max_val = pivot.values.max()
    
    for i, author in enumerate(authors):
        for j, year in enumerate(years):
            val = pivot.loc[author, year]
            xpos.append(i)
            ypos.append(j)
            zpos.append(0)
            dx.append(0.8)
            dy.append(0.8)
            dz.append(val)
            colors.append(cmap(val / max_val))
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, alpha=0.8, edgecolor='white')
    
    ax.set_xticks(range(len(authors)))
    ax.set_xticklabels([a[:10] for a in authors], rotation=45, fontsize=8)
    ax.set_yticks(range(len(years)))
    ax.set_yticklabels(years)
    
    ax.set_xlabel('作者', fontsize=12, fontweight='bold')
    ax.set_ylabel('年份', fontsize=12, fontweight='bold')
    ax.set_zlabel('提交数', fontsize=12, fontweight='bold')
    ax.set_title(f'3D Top{top_n}作者年度活跃度', fontsize=16, fontweight='bold', pad=20)
    
    ax.view_init(elev=20, azim=135)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/author_3d.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 3D作者图: {output_dir}/author_3d.png")
