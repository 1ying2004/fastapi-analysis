from src.collectors.git_collector import get_commits, save_to_csv, save_to_json, get_file_stats
from src.collectors.github_api import GitHubAPI
from src.analyzers.ast_analyzer import analyze_file, calculate_complexity
from src.analyzers.stats import generate_report
from src.visualizers.charts import plot_commits_by_year, plot_author_pie, generate_wordcloud
from src.visualizers.heatmap import plot_commit_heatmap
from src.visualizers.report import generate_html_report
from src.config import REPO_PATH, DATA_DIR, OUTPUT_DIR, GITHUB_REPO
import os

def main():
    print("=" * 60)
    print("  FastAPI 仓库分析工具  ")
    print("=" * 60)
    
    # 确保目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. 采集数据
    print("\n[1/4] 采集Git历史...")
    commits = get_commits(REPO_PATH)
    if not commits:
        print("   错误：无法获取提交数据")
        return
    
    print(f"   获取 {len(commits)} 条提交")
    save_to_csv(commits, DATA_DIR)
    save_to_json(commits, DATA_DIR)
    
    # 2. 统计分析
    print("\n[2/4] 统计分析...")
    report = generate_report(commits)
    print(f"   贡献者: {report['unique_authors']}")
    
    # 3. 可视化
    print("\n[3/4] 生成图表...")
    plot_commits_by_year(commits, OUTPUT_DIR)
    plot_author_pie(commits, OUTPUT_DIR)
    plot_commit_heatmap(commits, OUTPUT_DIR)
    
    # 词云
    text = ' '.join(c['message'] for c in commits)
    generate_wordcloud(text, OUTPUT_DIR)
    
    # 4. 报告
    print("\n[4/4] 生成报告...")
    generate_html_report(commits)
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print(f"  数据: {DATA_DIR}/")
    print(f"  图表: {OUTPUT_DIR}/")
    print("=" * 60)

if __name__ == '__main__':
    main()
