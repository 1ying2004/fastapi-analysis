"""
趋势图可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.config import CHART_DPI

def setup():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

def plot_monthly_trend(commits, output_dir='output'):
    """月度提交趋势"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['month'] = df['date'].dt.to_period('M')
    
    monthly = df.groupby('month').size()
    
    plt.figure(figsize=(16, 6))
    monthly.plot(kind='line', marker='o', linewidth=2, markersize=4)
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('提交数', fontsize=12)
    plt.title('月度提交趋势', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_trend.png', dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
    print(f"✓ 趋势图: {output_dir}/monthly_trend.png")

def plot_cumulative(commits, output_dir='output'):
    """累计提交曲线"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['date'] = df['date'].dt.date
    df = df.sort_values('date')
    df['cumulative'] = range(1, len(df) + 1)
    
    plt.figure(figsize=(14, 6))
    plt.fill_between(range(len(df)), df['cumulative'], alpha=0.4)
    plt.plot(df['cumulative'], linewidth=2)
    plt.xlabel('时间', fontsize=12)
    plt.ylabel('累计提交数', fontsize=12)
    plt.title('累计提交增长', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/cumulative.png', dpi=CHART_DPI, bbox_inches='tight')
    plt.close()
