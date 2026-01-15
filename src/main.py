"""
FastAPI仓库深度分析工具 - 主程序

集成所有分析模块，提供完整的仓库分析功能
使用技术栈：ast, libcst, pysnooper, z3-solver

用法:
    python src/main.py          # 完整分析（使用缓存数据）
    python src/main.py --fetch  # 仅获取全量数据（无限等待）
"""
import sys
import os
import warnings

from src.collectors.git_collector import get_commits, save_to_csv, save_to_json, get_file_stats
from src.collectors.branch_collector import get_branches
from src.collectors.tag_collector import get_tags
from src.collectors.issues_collector import IssuesCollector
from src.collectors.contributors_collector import ContributorsCollector
from src.analyzers.ast_analyzer import analyze_project_ast
from src.analyzers.stats import generate_report
from src.analyzers.message_analyzer import analyze_messages
from src.analyzers.loc_counter import analyze_project_loc
from src.analyzers.dependency_analyzer import build_dependency_graph
from src.analyzers.pr_analyzer import analyze_prs, analyze_issues
from src.visualizers.charts import plot_commits_by_year, plot_author_pie, generate_wordcloud
from src.visualizers.heatmap import plot_commit_heatmap
from src.visualizers.trends import plot_monthly_trend, plot_cumulative
from src.visualizers.author_charts import plot_top_authors
from src.visualizers.file_charts import plot_file_types, plot_loc_bar
from src.visualizers.complexity_charts import plot_complexity_distribution, plot_function_count_by_file
from src.visualizers.message_charts import plot_commit_types
from src.visualizers.yearly_charts import plot_yearly_comparison
from src.visualizers.dependency_charts import plot_import_frequency, plot_file_dependencies
from src.visualizers.issues_charts import plot_issues_by_state, plot_issues_timeline, plot_top_issue_authors
from src.visualizers.contributors_charts import plot_top_contributors, plot_contributions_distribution
from src.visualizers.pr_charts import plot_pr_state, plot_pr_timeline, plot_top_pr_authors
from src.visualizers.charts_3d import plot_3d_commits_by_year_month, plot_3d_author_activity
from src.visualizers.font_config import configure_matplotlib
from src.utils.persistence import ensure_data_dirs, save_json
from src.config import REPO_PATH, DATA_DIR, OUTPUT_DIR, GITHUB_REPO

warnings.filterwarnings('ignore')
configure_matplotlib()


def fetch_all_data():
    """仅获取全量数据模式（无超时限制）"""
    print("=" * 70)
    print("   数据获取模式 - 获取全量GitHub数据")
    print("   注意: 此模式会完整等待API限流")
    print("=" * 70)
    
    ensure_data_dirs()
    
    print("\n[1/4] Git数据...")
    commits = get_commits(REPO_PATH)
    print(f"  ✓ 提交: {len(commits):,}")
    save_to_csv(commits, DATA_DIR)
    save_to_json(commits, DATA_DIR)
    
    print("\n[2/4] Issues...")
    from src.collectors.issues_collector_full import IssuesCollectorFull
    collector = IssuesCollectorFull(GITHUB_REPO)
    issues = collector.fetch_all_issues()
    print(f"  ✓ Issues: {len(issues)}")
    
    print("\n[3/4] Pull Requests...")
    prs = collector.fetch_all_prs()
    print(f"  ✓ PRs: {len(prs)}")
    
    print("\n[4/4] Contributors...")
    from src.collectors.contributors_collector_full import ContributorsCollectorFull
    contrib_collector = ContributorsCollectorFull(GITHUB_REPO)
    contributors = contrib_collector.fetch_all()
    print(f"  ✓ Contributors: {len(contributors)}")
    
    print("\n" + "=" * 70)
    print("数据获取完成!")
    print("=" * 70)


def main():
    """主程序入口"""
    print("=" * 70)
    print("   FastAPI 仓库深度分析工具   ")
    print("   技术栈: ast | libcst | pysnooper | z3-solver   ")
    print("=" * 70)
    
    ensure_data_dirs()
    
    print("\n" + "=" * 70)
    print("[1/5] Git数据采集")
    print("=" * 70)
    
    commits = get_commits(REPO_PATH)
    if not commits:
        print("  ✗ 无法获取提交")
        return
    
    print(f"  ✓ Git提交: {len(commits):,} 条")
    save_to_csv(commits, DATA_DIR)
    save_to_json(commits, DATA_DIR)
    
    file_stats = get_file_stats(REPO_PATH)
    branches = get_branches(REPO_PATH)
    tags = get_tags(REPO_PATH)
    print(f"  ✓ 分支: {len(branches)} | 标签: {len(tags)}")
    
    print("\n" + "=" * 70)
    print("[2/5] GitHub数据采集")
    print("=" * 70)
    
    issues_collector = IssuesCollector(GITHUB_REPO)
    contributors_collector = ContributorsCollector(GITHUB_REPO)
    
    print("  采集Issues...")
    issues = issues_collector.fetch_issues()
    issues_collector.save_issues(issues)
    print(f"  ✓ Issues: {len(issues)} 条")
    
    print("  采集PRs...")
    prs = issues_collector.fetch_pull_requests()
    issues_collector.save_prs(prs)
    print(f"  ✓ PRs: {len(prs)} 条")
    
    print("  采集贡献者...")
    contributors = contributors_collector.fetch_contributors()
    contributors_collector.save_contributors(contributors)
    print(f"  ✓ 贡献者: {len(contributors)} 位")
    
    print("\n" + "=" * 70)
    print("[3/5] AST代码分析")
    print("=" * 70)
    
    ast_results = analyze_project_ast(REPO_PATH)
    summary = ast_results.get('summary', {})
    print(f"  ✓ 分析文件: {summary.get('total_files', 0)}")
    print(f"  ✓ 函数: {summary.get('total_functions', 0)}")
    print(f"  ✓ 类: {summary.get('total_classes', 0)}")
    
    save_json(ast_results, os.path.join(DATA_DIR, 'ast_analysis.json'))
    
    print("\n" + "=" * 70)
    print("[4/5] 统计分析")
    print("=" * 70)
    
    report = generate_report(commits)
    msg_stats = analyze_messages(commits)
    loc_stats = analyze_project_loc(REPO_PATH)
    dep_graph = build_dependency_graph(REPO_PATH)
    
    print(f"  ✓ 贡献者: {report['unique_authors']}")
    print(f"  ✓ 代码行数: {loc_stats['code']:,}")
    print(f"  ✓ 注释行数: {loc_stats['comment']:,}")
    
    save_json(report, os.path.join(DATA_DIR, 'report.json'))
    save_json(loc_stats, os.path.join(DATA_DIR, 'loc_stats.json'))
    save_json(msg_stats, os.path.join(DATA_DIR, 'message_stats.json'))
    
    print("\n" + "=" * 70)
    print("[5/5] 生成图表")
    print("=" * 70)
    
    plot_commits_by_year(commits, OUTPUT_DIR)
    plot_author_pie(commits, OUTPUT_DIR)
    plot_top_authors(commits, OUTPUT_DIR)
    plot_commit_heatmap(commits, OUTPUT_DIR)
    plot_monthly_trend(commits, OUTPUT_DIR)
    plot_cumulative(commits, OUTPUT_DIR)
    plot_file_types(file_stats, OUTPUT_DIR)
    plot_loc_bar(loc_stats, OUTPUT_DIR)
    plot_complexity_distribution(ast_results, OUTPUT_DIR)
    plot_function_count_by_file(ast_results, OUTPUT_DIR)
    plot_commit_types(msg_stats, OUTPUT_DIR)
    plot_yearly_comparison(commits, OUTPUT_DIR)
    plot_import_frequency(dep_graph, OUTPUT_DIR)
    plot_file_dependencies(dep_graph, OUTPUT_DIR)
    
    if issues:
        plot_issues_by_state(issues, OUTPUT_DIR)
        plot_issues_timeline(issues, OUTPUT_DIR)
        plot_top_issue_authors(issues, OUTPUT_DIR)
        issues_analysis = analyze_issues(issues)
        save_json(issues_analysis, os.path.join(DATA_DIR, 'issues_analysis.json'))
    
    if prs:
        plot_pr_state(prs, OUTPUT_DIR)
        plot_pr_timeline(prs, OUTPUT_DIR)
        plot_top_pr_authors(prs, OUTPUT_DIR)
        prs_analysis = analyze_prs(prs)
        save_json(prs_analysis, os.path.join(DATA_DIR, 'prs_analysis.json'))
    
    if contributors:
        plot_top_contributors(contributors, OUTPUT_DIR)
        plot_contributions_distribution(contributors, OUTPUT_DIR)
    
    plot_3d_commits_by_year_month(commits, OUTPUT_DIR)
    plot_3d_author_activity(commits, OUTPUT_DIR)
    
    text = ' '.join(c['message'] for c in commits)
    generate_wordcloud(text, OUTPUT_DIR)
    
    summary_data = {
        'total_commits': len(commits),
        'contributors': report['unique_authors'],
        'github_contributors': len(contributors),
        'issues': len(issues),
        'prs': len(prs),
        'branches': len(branches),
        'tags': len(tags),
        'code_lines': loc_stats['code'],
        'functions': summary.get('total_functions', 0),
        'classes': summary.get('total_classes', 0),
        'message_types': msg_stats
    }
    save_json(summary_data, os.path.join(OUTPUT_DIR, 'summary.json'))
    
    print("\n" + "=" * 70)
    print("分析完成!")
    print("=" * 70)
    
    print(f"\n  📁 数据目录: {DATA_DIR}/")
    for f in os.listdir(DATA_DIR):
        print(f"      • {f}")
    
    print(f"\n  📊 图表目录: {OUTPUT_DIR}/")
    chart_count = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
    print(f"      共 {chart_count} 张图表")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--fetch':
        fetch_all_data()
    else:
        main()
