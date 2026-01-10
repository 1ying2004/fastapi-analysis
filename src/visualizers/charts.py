import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
if os.path.exists(FONT_PATH):
    fm.fontManager.addfont(FONT_PATH)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def plot_commits_by_year(commits_data, output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    
    years = {}
    for commit in commits_data:
        year = commit['date'][:4]
        years[year] = years.get(year, 0) + 1
    
    plt.figure(figsize=(14, 7))
    bars = plt.bar(list(years.keys()), list(years.values()), color='#667eea')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.xlabel('年份', fontsize=14)
    plt.ylabel('提交数', fontsize=14)
    plt.title('年度提交统计', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'commits_by_year.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"图表已保存到 {output_dir}/commits_by_year.png")
