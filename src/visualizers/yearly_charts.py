"""
年度对比可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

def plot_yearly_comparison(commits, output_dir='output'):
    """年度对比图"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    yearly = df.groupby(['year', 'month']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    for year in yearly.index:
        ax.plot(range(1, 13), yearly.loc[year], marker='o', 
                linewidth=2, markersize=6, label=str(year))
    
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['1月','2月','3月','4月','5月','6月',
                        '7月','8月','9月','10月','11月','12月'])
    ax.set_xlabel('月份', fontsize=14, fontweight='bold')
    ax.set_ylabel('提交数', fontsize=14, fontweight='bold')
    ax.set_title('各年度月度提交对比', fontsize=18, fontweight='bold', pad=20)
    ax.legend(title='年度', loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yearly_comparison.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 年度对比: {output_dir}/yearly_comparison.png")
