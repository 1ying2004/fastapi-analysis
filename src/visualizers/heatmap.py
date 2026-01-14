import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.config import CHART_DPI, FONT_PATH

def setup_style():
    """设置绘图风格"""
    sns.set_style("whitegrid")
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.dpi'] = CHART_DPI

def plot_commit_heatmap(commits_data, output_dir='output'):
    """绘制提交热力图"""
    setup_style()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits_data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['weekday'] = df['date'].dt.dayofweek
    df['hour'] = df['date'].dt.hour
    
    pivot = df.groupby(['weekday', 'hour']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(14, 6))
    sns.heatmap(pivot, cmap='YlOrRd', annot=False,
                xticklabels=range(24),
                yticklabels=['周一','周二','周三','周四','周五','周六','周日'])
    plt.xlabel('小时', fontsize=12)
    plt.ylabel('星期', fontsize=12)
    plt.title('提交时间热力图', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/commit_heatmap.png', dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    print(f"✓ 保存: {output_dir}/commit_heatmap.png")
