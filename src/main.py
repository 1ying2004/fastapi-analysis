"""
FastAPI仓库深度分析工具 - 主程序
"""
from src.collectors.git_collector import get_commits, save_to_csv, save_to_json, get_file_stats
from src.collectors.github_api import GitHubAPI
from src.collectors.branch_collector import get_branches
from src.collectors.tag_collector import get_tags
from src.analyzers.ast_analyzer import analyze_project_ast
from src.analyzers.stats import generate_report
from src.analyzers.message_analyzer import analyze_messages
from src.analyzers.loc_counter import analyze_project_loc
from src.visualizers.charts import plot_commits_by_year, plot_author_pie, generate_wordcloud
from src.visualizers.heatmap import plot_commit_heatmap
from src.visualizers.trends import plot_monthly_trend
from src.visualizers.author_charts import plot_top_authors
from src.visualizers.file_charts import plot_file_types, plot_loc_bar
from src.visualizers.complexity_charts import plot_complexity_distribution, plot_function_count_by_file
from src.visualizers.report import generate_html_report
from src.visualizers.font_config import configure_matplotlib
from src.utils.validator import run_checks, ensure_directories
from src.config import REPO_PATH, DATA_DIR, OUTPUT_DIR
import os
import json
import warnings

warnings.filterwarnings('ignore')
configure_matplotlib()

def main():
    print("=" * 70)
    print("   FastAPI 仓库深度分析工具   ")
    print("   使用 ast | libcst | pysnooper | z3-solver   ")
    print("=" * 70)
    
    print("\n[准备] 环境检查...")
    checks = run_checks()
    for name, (ok, msg) in checks.items():
        status = "✓" if ok else "✗"
        print(f"  {status} {name}: {msg}")
    
    ensure_directories()
    
    print("\n" + "=" * 70)
    print("[1/6] 数据采集")
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
    print("[2/6] 代码分析 (AST)")
    print("=" * 70)
    
    ast_results = analyze_project_ast(REPO_PATH)
    summary = ast_results.get('summary', {})
    print(f"  ✓ 文件: {summary.get('total_files', 0)}")
    print(f"  ✓ 函数: {summary.get('total_functions', 0)}")
    print(f"  ✓ 类: {summary.get('total_classes', 0)}")
    
    with open(os.path.join(DATA_DIR, 'ast_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(ast_results, f, ensure_ascii=False, indent=2, default=str)
    print(f"  ✓ AST分析结果已保存")
    
    print("\n" + "=" * 70)
    print("[3/6] 统计分析")
    print("=" * 70)
    
    report = generate_report(commits)
    msg_stats = analyze_messages(commits)
    loc_stats = analyze_project_loc(REPO_PATH)
    
    print(f"  ✓ 贡献者: {report['unique_authors']}")
    print(f"  ✓ 代码行数: {loc_stats['code']:,}")
    print(f"  ✓ 注释行数: {loc_stats['comment']:,}")
    
    print("\n" + "=" * 70)
    print("[4/6] 生成图表")
    print("=" * 70)
    
    plot_commits_by_year(commits, OUTPUT_DIR)
    plot_author_pie(commits, OUTPUT_DIR)
    plot_top_authors(commits, OUTPUT_DIR)
    plot_commit_heatmap(commits, OUTPUT_DIR)
    plot_monthly_trend(commits, OUTPUT_DIR)
    plot_file_types(file_stats, OUTPUT_DIR)
    plot_loc_bar(loc_stats, OUTPUT_DIR)
    
    plot_complexity_distribution(ast_results, OUTPUT_DIR)
    plot_function_count_by_file(ast_results, OUTPUT_DIR)
    
    text = ' '.join(c['message'] for c in commits)
    generate_wordcloud(text, OUTPUT_DIR)
    
    print("\n" + "=" * 70)
    print("[5/6] 生成报告")
    print("=" * 70)
    
    generate_html_report(commits)
    
    with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
        summary_data = {
            'total_commits': len(commits),
            'contributors': report['unique_authors'],
            'branches': len(branches),
            'tags': len(tags),
            'code_lines': loc_stats['code'],
            'functions': summary.get('total_functions', 0),
            'classes': summary.get('total_classes', 0),
            'message_types': msg_stats
        }
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 摘要JSON已保存")
    
    print("\n" + "=" * 70)
    print("[6/6] 完成!")
    print("=" * 70)
    
    print(f"\n  📁 数据目录: {DATA_DIR}/")
    print(f"  📊 图表目录: {OUTPUT_DIR}/")
    print(f"\n  生成的图表:")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.png'):
            print(f"    • {f}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
