"""
热力图可视化
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_commit_heatmap(commits_data, output_dir='output'):
    """绘制提交热力图"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits_data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['weekday'] = df['date'].dt.dayofweek
    df['hour'] = df['date'].dt.hour
    
    pivot = df.groupby(['weekday', 'hour']).size().unstack(fill_value=0)
    
    for i in range(7):
        if i not in pivot.index:
            pivot.loc[i] = 0
    pivot = pivot.sort_index()
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    sns.heatmap(pivot, cmap='YlOrRd', annot=False, ax=ax,
                cbar_kws={'label': '提交数'})
    
    ax.set_xticklabels(range(24), fontsize=10)
    ax.set_yticklabels(['周一','周二','周三','周四','周五','周六','周日'], 
                       fontsize=11, rotation=0)
    ax.set_xlabel('小时', fontsize=14, fontweight='bold')
    ax.set_ylabel('星期', fontsize=14, fontweight='bold')
    ax.set_title('提交时间热力图', fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/commit_heatmap.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 热力图: {output_dir}/commit_heatmap.png")
