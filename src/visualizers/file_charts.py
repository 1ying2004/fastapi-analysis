"""
文件变更可视化
"""
import matplotlib.pyplot as plt
import os

def setup():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

def plot_file_types(file_stats, output_dir='output'):
    """绘制文件类型分布"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    sorted_stats = sorted(file_stats.items(), key=lambda x: -x[1])[:10]
    
    labels = [s[0] for s in sorted_stats]
    values = [s[1] for s in sorted_stats]
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.Set3(range(len(labels)))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.title('文件类型分布', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/file_types.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 保存: {output_dir}/file_types.png")

def plot_loc_bar(loc_data, output_dir='output'):
    """绘制代码行数柱状图"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    categories = ['代码行', '空行', '注释行']
    values = [loc_data['code'], loc_data['blank'], loc_data['comment']]
    colors = ['#667eea', '#a8a8a8', '#48bb78']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color=colors)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height):,}', ha='center', va='bottom')
    
    plt.ylabel('行数', fontsize=12)
    plt.title('代码行数统计', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/loc_bar.png', dpi=150, bbox_inches='tight')
    plt.close()
