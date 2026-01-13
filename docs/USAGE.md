# 使用说明

## 环境要求

- Python 3.8+
- Windows/Linux/macOS

## 安装依赖

```bash
pip install -r requirements.txt
```

## 基本使用

### 1. 分析本地仓库

```python
from src.collectors.git_collector import get_commits

commits = get_commits('/path/to/repo')
print(f"共 {len(commits)} 条提交")
```

### 2. 分析GitHub仓库

```python
from src.collectors.github_api import GitHubAPI

api = GitHubAPI('tiangolo/fastapi')
issues = api.get_issues()
```

### 3. 生成图表

```python
from src.visualizers.charts import plot_commits_by_year

plot_commits_by_year(commits)
```

### 4. 代码分析

```python
from src.analyzers.ast_analyzer import analyze_file

result = analyze_file('example.py')
print(result['functions'])
```

## 命令行使用

```bash
# 运行完整分析
python src/main.py

# 只获取数据
python -c "from src.collectors.git_collector import get_commits; print(get_commits('.'))"
```

## 输出说明

- `data/` - 数据文件（CSV, JSON）
- `output/` - 图表文件（PNG）
- `cache/` - 缓存数据
