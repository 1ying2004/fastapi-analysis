# API 文档

## collectors 模块

### git_collector

```python
get_commits(repo_path, max_count=10000)
```
获取Git提交历史

**参数:**
- `repo_path`: 仓库路径
- `max_count`: 最大提交数

**返回:** 提交列表

---

### github_api

```python
GitHubAPI(repo, token=None)
```
GitHub API客户端

**方法:**
- `get_issues()` - 获取issues
- `get_contributors()` - 获取贡献者

---

## analyzers 模块

### ast_analyzer

```python
analyze_file(filepath)
```
分析Python文件AST

```python
calculate_complexity(filepath)
```
计算代码复杂度

---

## visualizers 模块

### charts

```python
plot_commits_by_year(commits, output_dir)
plot_author_pie(commits, output_dir)
generate_wordcloud(text, output_dir)
```

生成各类图表
