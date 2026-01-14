# 使用说明

## 环境准备

1. Python 3.8+
2. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行分析

```bash
# 进入项目目录
cd fastapi-analysis

# 运行分析
python src/main.py
```

## 输出目录

```
data/      - 采集的数据
├── commits.csv
├── commits.json
└── ast_analysis.json

output/    - 可视化图表
├── commits_by_year.png
├── authors_pie.png
├── commit_heatmap.png
└── ...

logs/      - 运行日志

cache/     - API缓存
```

## 分析模块

### AST分析

```python
from src.analyzers.ast_analyzer import analyze_project_ast
result = analyze_project_ast('/path/to/project')
```

### libcst分析

```python
from src.analyzers.libcst_analyzer import analyze_with_libcst
result = analyze_with_libcst('/path/to/file.py')
```

### pysnooper追踪

```python
from src.analyzers.dynamic_tracer import demo_pysnooper
demo_pysnooper()
```

### z3符号执行

```python
from src.analyzers.z3_analysis import symbolic_execution_demo
symbolic_execution_demo()
```
