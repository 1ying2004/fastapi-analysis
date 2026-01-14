"""
趋势图可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_monthly_trend(commits, output_dir='output'):
    """月度提交趋势"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['month'] = df['date'].dt.to_period('M')
    
    monthly = df.groupby('month').size()
    
    fig, ax = plt.subplots(figsize=(18, 7))
    
    x = range(len(monthly))
    ax.fill_between(x, monthly.values, alpha=0.3, color='#667eea')
    ax.plot(x, monthly.values, marker='o', linewidth=2, markersize=4, color='#667eea')
    
    step = max(1, len(monthly) // 20)
    ax.set_xticks(x[::step])
    ax.set_xticklabels([str(m) for m in monthly.index[::step]], rotation=45, ha='right', fontsize=9)
    
    ax.set_xlabel('月份', fontsize=14, fontweight='bold')
    ax.set_ylabel('提交数', fontsize=14, fontweight='bold')
    ax.set_title('月度提交趋势', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_trend.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 月度趋势: {output_dir}/monthly_trend.png")

def plot_cumulative(commits, output_dir='output'):
    """累计提交曲线"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df = df.sort_values('date')
    df['cumulative'] = range(1, len(df) + 1)
    
    fig, ax = plt.subplots(figsize=(16, 7))
    
    ax.fill_between(range(len(df)), df['cumulative'], alpha=0.4, color='#48bb78')
    ax.plot(df['cumulative'].values, linewidth=2, color='#48bb78')
    
    ax.set_xlabel('时间', fontsize=14, fontweight='bold')
    ax.set_ylabel('累计提交数', fontsize=14, fontweight='bold')
    ax.set_title('累计提交增长曲线', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    total = len(df)
    ax.annotate(f'总计: {total:,}', xy=(len(df)-1, total), 
                fontsize=14, fontweight='bold', color='#48bb78')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/cumulative.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 累计曲线: {output_dir}/cumulative.png")
