from src.collectors.git_collector import get_commits, save_to_csv, save_to_json, get_file_stats
from src.collectors.github_api import GitHubAPI
from src.collectors.branch_collector import get_branches, get_current_branch
from src.collectors.tag_collector import get_tags, get_all_tags_info
from src.analyzers.ast_analyzer import analyze_file, calculate_complexity
from src.analyzers.stats import generate_report
from src.analyzers.message_analyzer import analyze_messages, extract_keywords
from src.analyzers.loc_counter import analyze_project_loc
from src.visualizers.charts import plot_commits_by_year, plot_author_pie, generate_wordcloud
from src.visualizers.heatmap import plot_commit_heatmap
from src.visualizers.trends import plot_monthly_trend, plot_cumulative
from src.visualizers.author_charts import plot_top_authors
from src.visualizers.file_charts import plot_file_types, plot_loc_bar
from src.visualizers.report import generate_html_report
from src.utils.validator import run_checks, ensure_directories
from src.config import REPO_PATH, DATA_DIR, OUTPUT_DIR
import os

def main():
    print("=" * 60)
    print("  FastAPI 仓库深度分析工具  ")
    print("=" * 60)
    
    # 检查环境
    print("\n[准备] 检查环境...")
    checks = run_checks()
    for name, (ok, msg) in checks.items():
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {msg}")
    
    ensure_directories()
    
    # 1. 采集
    print("\n[1/5] 采集Git数据...")
    commits = get_commits(REPO_PATH)
    if not commits:
        print("  ✗ 无法获取提交")
        return
    
    print(f"  ✓ {len(commits)} 条提交")
    save_to_csv(commits, DATA_DIR)
    save_to_json(commits, DATA_DIR)
    
    # 文件统计
    file_stats = get_file_stats(REPO_PATH)
    
    # 分支标签
    branches = get_branches(REPO_PATH)
    tags = get_tags(REPO_PATH)
    print(f"  ✓ {len(branches)} 分支, {len(tags)} 标签")
    
    # 2. 分析
    print("\n[2/5] 数据分析...")
    report = generate_report(commits)
    msg_stats = analyze_messages(commits)
    loc_stats = analyze_project_loc(REPO_PATH)
    print(f"  ✓ {report['unique_authors']} 贡献者")
    print(f"  ✓ {loc_stats['code']} 行代码")
    
    # 3. 可视化
    print("\n[3/5] 生成图表...")
    plot_commits_by_year(commits, OUTPUT_DIR)
    plot_author_pie(commits, OUTPUT_DIR)
    plot_top_authors(commits, OUTPUT_DIR)
    plot_commit_heatmap(commits, OUTPUT_DIR)
    plot_monthly_trend(commits, OUTPUT_DIR)
    plot_file_types(file_stats,OUTPUT_DIR)
    plot_loc_bar(loc_stats, OUTPUT_DIR)
    
    # 词云
    text = ' '.join(c['message'] for c in commits)
    generate_wordcloud(text, OUTPUT_DIR)
    
    # 4. 报告
    print("\n[4/5] 生成报告...")
    generate_html_report(commits)
    
    # 5. 完成
    print("\n[5/5] 完成!")
    print("\n" + "=" * 60)
    print(f"  数据: {DATA_DIR}/")
    print(f"  图表: {OUTPUT_DIR}/")
    print("=" * 60)

if __name__ == '__main__':
    main()
