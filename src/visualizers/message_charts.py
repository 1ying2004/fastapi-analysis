"""
消息类型可视化
"""
import matplotlib.pyplot as plt
import os

def setup():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False

def plot_message_types(msg_stats, output_dir='output'):
    """消息类型饼图"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    labels = list(msg_stats.keys())
    values = list(msg_stats.values())
    
    colors = ['#667eea', '#48bb78', '#ed8936', '#f56565', 
              '#9f7aea', '#38b2ac', '#a0aec0', '#fc8181']
    
    plt.figure(figsize=(12, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
    plt.title('提交类型分布', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/message_types.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 保存: {output_dir}/message_types.png")

def plot_message_bar(msg_stats, output_dir='output'):
    """消息类型柱状图"""
    setup()
    os.makedirs(output_dir, exist_ok=True)
    
    sorted_stats = sorted(msg_stats.items(), key=lambda x: -x[1])
    labels = [s[0] for s in sorted_stats]
    values = [s[1] for s in sorted_stats]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, values, color='#667eea')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.xlabel('类型', fontsize=12)
    plt.ylabel('数量', fontsize=12)
    plt.title('提交类型统计', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/message_bar.png', dpi=150, bbox_inches='tight')
    plt.close()
