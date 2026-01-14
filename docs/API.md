# API参考

## 数据采集

### git_collector

```python
get_commits(repo_path, max_count=10000) -> List[dict]
get_file_stats(repo_path) -> Dict[str, int]
save_to_csv(commits, output_dir='data')
save_to_json(commits, output_dir='data')
```

### github_api

```python
GitHubAPI(repo, token=None)
  .get_issues(state='all') -> List[dict]
  .get_contributors() -> List[dict]
```

## 代码分析

### ast_analyzer

```python
deep_analyze_file(filepath) -> Dict
analyze_project_ast(project_path) -> Dict
```

### libcst_analyzer

```python
analyze_with_libcst(filepath) -> Dict
analyze_project_libcst(project_path) -> Dict
```

### stats

```python
generate_report(commits) -> Dict
```

## 可视化

### charts

```python
plot_commits_by_year(commits_data, output_dir)
plot_author_pie(commits_data, output_dir)
generate_wordcloud(text_data, output_dir)
```

### heatmap

```python
plot_commit_heatmap(commits_data, output_dir)
```

### trends

```python
plot_monthly_trend(commits, output_dir)
plot_cumulative(commits, output_dir)
```
