# API参考文档

本文档列出项目所有公共API接口。

## 数据采集模块 (src/collectors)

### git_collector

本地Git仓库数据采集。

```python
get_commits(repo_path, max_count=10000) -> List[dict]
    """获取Git提交历史"""
    # 返回: [{hash, author, email, date, message}, ...]

get_file_stats(repo_path) -> Dict[str, int]
    """统计各类型文件数量"""
    # 返回: {'.py': 1252, '.md': 186, ...}

save_to_csv(commits, output_dir='data')
    """保存为CSV格式"""

save_to_json(commits, output_dir='data')
    """保存为JSON格式"""
```

### issues_collector / issues_collector_full

GitHub Issues采集。

```python
IssuesCollector(repo, token=None)
    .fetch_issues(state='all') -> List[dict]
    .fetch_pull_requests(state='all') -> List[dict]
    .save_issues(issues, filename='issues.json')
    .save_prs(prs, filename='pull_requests.json')

IssuesCollectorFull(repo, token=None)
    """全量采集版本，支持断点续传和指数退避"""
    .fetch_all_issues() -> List[dict]
    .fetch_all_prs() -> List[dict]
```

### contributors_collector

贡献者数据采集。

```python
ContributorsCollector(repo, token=None)
    .fetch_contributors() -> List[dict]
    .save_contributors(contributors)
    .get_stats(contributors) -> Dict
```

## 代码分析模块 (src/analyzers)

### ast_analyzer

基于Python AST的静态分析。

```python
deep_analyze_file(filepath) -> Dict
    """深度分析单个文件"""
    # 返回: {filepath, functions, classes, imports, avg_complexity, ...}

analyze_project_ast(project_path) -> Dict
    """分析整个项目"""
    # 返回: {files: [...], summary: {total_files, total_functions, total_classes}}
```

### libcst_analyzer

基于LibCST的代码结构分析。

```python
analyze_with_libcst(filepath) -> Dict
    """使用LibCST分析文件"""

analyze_project_libcst(project_path) -> Dict
    """分析整个项目"""
```

### dynamic_tracer

基于pysnooper的动态追踪。

```python
@pysnooper.snoop(depth=2)
def traced_commit_analyzer(commits) -> Dict
    """带追踪的提交分析示例"""

trace_function(func, *args, output_file=None) -> Tuple[Any, str]
    """追踪任意函数执行"""

demo_pysnooper()
    """pysnooper演示"""
```

### z3_analysis

基于Z3的符号执行。

```python
solve_integer_constraints(constraints_str) -> Dict
    """求解整数约束"""

analyze_branch_conditions(code_string) -> List[Dict]
    """分析代码分支条件"""

symbolic_execution_demo() -> Dict
    """符号执行演示"""

analyze_array_bounds() -> Dict
    """数组越界分析示例"""
```

### stats / message_analyzer / pr_analyzer

统计分析。

```python
generate_report(commits) -> Dict
    """生成统计报告"""

analyze_messages(commits) -> Dict
    """分析提交消息类型分布"""

analyze_prs(prs) -> Dict
    """分析PR数据"""

analyze_issues(issues) -> Dict
    """分析Issues数据"""
```

## 可视化模块 (src/visualizers)

### 基础图表

```python
# charts.py
plot_commits_by_year(commits, output_dir)
plot_author_pie(commits, output_dir)
generate_wordcloud(text, output_dir)

# heatmap.py
plot_commit_heatmap(commits, output_dir)

# trends.py
plot_monthly_trend(commits, output_dir)
plot_cumulative(commits, output_dir)
```

### 专题图表

```python
# author_charts.py
plot_top_authors(commits, output_dir, top_n=15)

# file_charts.py
plot_file_types(file_stats, output_dir)
plot_loc_bar(loc_stats, output_dir)

# complexity_charts.py
plot_complexity_distribution(ast_results, output_dir)
plot_function_count_by_file(ast_results, output_dir)

# issues_charts.py
plot_issues_by_state(issues, output_dir)
plot_issues_timeline(issues, output_dir)
plot_top_issue_authors(issues, output_dir)

# pr_charts.py
plot_pr_state(prs, output_dir)
plot_pr_timeline(prs, output_dir)
plot_top_pr_authors(prs, output_dir)

# contributors_charts.py
plot_top_contributors(contributors, output_dir)
plot_contributions_distribution(contributors, output_dir)

# charts_3d.py
plot_3d_commits_by_year_month(commits, output_dir)
plot_3d_author_activity(commits, output_dir)
```

### 字体配置

```python
# font_config.py
configure_matplotlib()
    """配置matplotlib全局中文支持"""

get_font_prop() -> FontProperties
    """获取中文字体属性对象"""
```

## 工具模块 (src/utils)

```python
# persistence.py
ensure_data_dirs()
save_json(data, filepath)
load_json(filepath) -> Any

# cache.py
FileCache(cache_dir='cache')
    .get(key) -> Any
    .set(key, value, ttl=3600)
    .clear()

# helpers.py
safe_divide(a, b, default=0) -> float
format_number(n) -> str
truncate_str(s, max_len=50) -> str
```
