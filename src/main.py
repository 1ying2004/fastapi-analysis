from src.collectors.git_collector import get_commits, save_to_csv, save_to_json
from src.collectors.github_api import GitHubAPI
from src.analyzers.ast_analyzer import analyze_file, calculate_complexity
from src.visualizers.charts import plot_commits_by_year, generate_wordcloud
import os

REPO_PATH = '../../fastapi'
DATA_DIR = 'data'
OUTPUT_DIR = 'output'

def main():
    print("=" * 50)
    print("FastAPI 仓库分析工具")
    print("=" * 50)
    
    # 采集git数据
    print("\n[1/3] 正在采集Git历史...")
    commits = get_commits(REPO_PATH)
    
    if commits:
        os.makedirs(DATA_DIR, exist_ok=True)
        save_to_csv(commits, DATA_DIR)
        save_to_json(commits, DATA_DIR)
        print(f"    共 {len(commits)} 个提交")
    
    # 可视化
    print("\n[2/3] 生成图表...")
    if commits:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        plot_commits_by_year(commits, OUTPUT_DIR)
        
        # 词云
        text = ' '.join([c['message'] for c in commits])
        generate_wordcloud(text, OUTPUT_DIR)
    
    # 完成
    print("\n[3/3] 分析完成")
    print(f"    数据: {DATA_DIR}/")
    print(f"    图表: {OUTPUT_DIR}/")
    print("=" * 50)

if __name__ == '__main__':
    main()
