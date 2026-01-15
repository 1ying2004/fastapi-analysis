"""
提交消息分析可视化

分析提交消息的类型、关键词等
"""
import matplotlib.pyplot as plt
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib

configure_matplotlib()

COMMIT_TYPE_NAMES = {
    'feat': '新功能',
    'feature': '新功能',
    'fix': '修复',
    'bugfix': '修复',
    'docs': '文档',
    'refactor': '重构',
    'test': '测试',
    'chore': '杂项',
    'style': '样式',
    'perf': '性能',
    'other': '其他'
}


def plot_commit_types(msg_stats, output_dir='output'):
    """
    提交类型综合分析图
    
    水平柱状图 + 百分比标注
    """
    os.makedirs(output_dir, exist_ok=True)
    
    sorted_stats = sorted(msg_stats.items(), key=lambda x: -x[1])
    total = sum(v for k, v in sorted_stats)
    
    labels = [COMMIT_TYPE_NAMES.get(s[0], s[0]) for s in sorted_stats]
    values = [s[1] for s in sorted_stats]
    percentages = [v / total * 100 for v in values]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(labels)))[::-1]
    bars = ax.barh(range(len(labels)), values, color=colors, edgecolor='white', height=0.7)
    
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=12)
    ax.invert_yaxis()
    
    for i, (bar, pct) in enumerate(zip(bars, percentages)):
        width = bar.get_width()
        ax.text(width + max(values)*0.01, bar.get_y() + bar.get_height()/2,
               f'{int(width):,} ({pct:.1f}%)', va='center', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('提交数量', fontsize=14, fontweight='bold')
    ax.set_title('提交类型分析', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    ax.text(0.95, 0.95, f'总计: {total:,} 条提交', transform=ax.transAxes,
           fontsize=12, ha='right', va='top', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/commit_types.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 提交类型: {output_dir}/commit_types.png")


def plot_message_types(msg_stats, output_dir='output'):
    """保留旧接口，调用新函数"""
    plot_commit_types(msg_stats, output_dir)


def plot_message_bar(msg_stats, output_dir='output'):
    """保留旧接口，不再生成图（避免重复）"""
    pass
