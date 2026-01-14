"""
作者统计可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.config import CHART_DPI

def setup():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

def plot_top_authors(commits, output_dir='output', top_n=15):
    """绘制top作者柱状图"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    top = df['author'].value_counts().head(top_n)
    
    plt.figure(figsize=(14, 8))
    bars = plt.barh(range(len(top)), top.values, color='#764ba2')
    plt.yticks(range(len(top)), top.index)
    
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                f'{int(bar.get_width())}', va='center')
    
    plt.xlabel('提交数', fontsize=12)
    plt.title(f'Top {top_n} 贡献者', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_authors.png', dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    print(f"✓ 保存: {output_dir}/top_authors.png")

def plot_author_activity(commits, author, output_dir='output'):
    """绘制单个作者活动"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df = df[df['author'] == author]
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    daily = df.groupby('date').size()
    
    plt.figure(figsize=(14, 5))
    daily.plot(kind='bar', color='#667eea', alpha=0.7)
    plt.title(f'{author} 提交活动', fontsize=14)
    plt.xlabel('日期')
    plt.ylabel('提交数')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/author_{author}_activity.png', dpi=CHART_DPI)
    plt.close()
