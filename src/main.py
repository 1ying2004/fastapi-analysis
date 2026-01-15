"""
FastAPI仓库深度分析工具 - 主程序

集成所有分析模块，提供完整的仓库分析功能
使用技术栈：ast, libcst, pysnooper, z3-solver

功能模块：
- Git历史采集和分析
- GitHub Issues/PR采集
- 贡献者分析
- AST静态代码分析
- 依赖关系分析
- 可视化图表生成
"""
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
from src.analyzers.health_scorer import generate_health_report
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
from src.visualizers.report import generate_html_report
from src.visualizers.font_config import configure_matplotlib
from src.utils.persistence import ensure_data_dirs, save_json
from src.config import REPO_PATH, DATA_DIR, OUTPUT_DIR, GITHUB_REPO
import os
import warnings

warnings.filterwarnings('ignore')
configure_matplotlib()


def main():
    """主程序入口"""
    print("=" * 70)
    print("   FastAPI 仓库深度分析工具   ")
    print("   技术栈: ast | libcst | pysnooper | z3-solver   ")
    print("=" * 70)
    
    ensure_data_dirs()
    
    # ========== 1. Git数据采集 ==========
    print("\n" + "=" * 70)
    print("[1/7] Git数据采集")
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
    
    # ========== 2. GitHub API采集 ==========
    print("\n" + "=" * 70)
    print("[2/7] GitHub数据采集 (Issues/PR/Contributors)")
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
    
    # ========== 3. AST代码分析 ==========
    print("\n" + "=" * 70)
    print("[3/7] AST代码分析")
    print("=" * 70)
    
    ast_results = analyze_project_ast(REPO_PATH)
    summary = ast_results.get('summary', {})
    print(f"  ✓ 分析文件: {summary.get('total_files', 0)}")
    print(f"  ✓ 函数: {summary.get('total_functions', 0)}")
    print(f"  ✓ 类: {summary.get('total_classes', 0)}")
    
    save_json(ast_results, os.path.join(DATA_DIR, 'ast_analysis.json'))
    
    # ========== 4. 统计分析 ==========
    print("\n" + "=" * 70)
    print("[4/7] 统计分析")
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
    
    # ========== 5. 健康评分 ==========
    print("\n" + "=" * 70)
    print("[5/7] 项目健康评分")
    print("=" * 70)
    
    issue_close_rate = 0
    if issues:
        closed = sum(1 for i in issues if i.get('state') == 'closed')
        issue_close_rate = closed / len(issues) * 100 if issues else 0
    
    pr_merge_rate = 0
    if prs:
        merged = sum(1 for p in prs if p.get('merged_at'))
        pr_merge_rate = merged / len(prs) * 100 if prs else 0
    
    health_metrics = {
        'total_commits': len(commits),
        'contributors': len(contributors),
        'avg_complexity': sum(f.get('complexity', 1) for file in ast_results.get('files', []) for f in file.get('functions', [])) / max(1, summary.get('total_functions', 1)),
        'issue_close_rate': issue_close_rate,
        'pr_merge_rate': pr_merge_rate
    }
    health_report = generate_health_report(health_metrics)
    print(f"  ✓ 健康评分: {health_report['score']} (等级: {health_report['grade']})")
    for key, val in health_report.get('details', {}).items():
        print(f"      {key}: {val}")
    save_json(health_report, os.path.join(DATA_DIR, 'health_report.json'))
    
    # ========== 6. 生成图表 ==========
    print("\n" + "=" * 70)
    print("[6/7] 生成图表")
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
    
    # ========== 7. 生成报告 ==========
    print("\n" + "=" * 70)
    print("[7/7] 生成报告")
    print("=" * 70)
    
    generate_html_report(commits)
    
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
        'health_score': health_report['score'],
        'health_grade': health_report['grade'],
        'message_types': msg_stats
    }
    save_json(summary_data, os.path.join(OUTPUT_DIR, 'summary.json'))
    
    # ========== 完成 ==========
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
    main()
