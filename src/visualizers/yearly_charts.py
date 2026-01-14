"""
年度对比可视化
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
from src.visualizers.style import apply_style

def plot_yearly_comparison(commits, output_dir='output'):
    """年度对比图"""
    apply_style()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    yearly = df.groupby(['year', 'month']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(14, 8))
    yearly.T.plot(kind='line', marker='o', ax=plt.gca())
    plt.xlabel('月份', fontsize=12)
    plt.ylabel('提交数', fontsize=12)
    plt.title('各年度月度提交对比', fontsize=14, fontweight='bold')
    plt.legend(title='年度', loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/yearly_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 保存: {output_dir}/yearly_comparison.png")
