import matplotlib.pyplot as plt
import os

def setup_chinese_font():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

def plot_commits_by_year(commits_data, output_dir='output'):
    setup_chinese_font()
    os.makedirs(output_dir, exist_ok=True)
    
    years = {}
    for commit in commits_data:
        year = commit['date'][:4]
        years[year] = years.get(year, 0) + 1
    
    plt.figure(figsize=(12, 6))
    plt.bar(years.keys(), years.values())
    plt.xlabel('Year')
    plt.ylabel('Commits')
    plt.title('Commits by Year')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'commits_by_year.png'), dpi=150)
    plt.close()
    
    print(f"Saved chart to {output_dir}/commits_by_year.png")
