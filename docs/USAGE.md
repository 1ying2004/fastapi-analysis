# 使用指南

## 快速开始

```bash
python src/main.py
```

## 输出目录结构

```
data/                    # 采集的数据
├── commits.csv          # 提交记录CSV
├── commits.json         # 提交记录JSON
├── ast_analysis.json    # AST分析结果
├── report.json          # 统计报告
└── loc_stats.json       # 代码行数统计

output/                  # 可视化结果
├── commits_by_year.png  # 年度提交图
├── authors_pie.png      # 贡献者饼图
├── commit_heatmap.png   # 热力图
├── monthly_trend.png    # 月度趋势
├── cumulative.png       # 累计增长
├── ...
└── report.html          # HTML报告
```

## 模块使用示例

### AST分析

```python
from src.analyzers.ast_analyzer import analyze_project_ast

result = analyze_project_ast('/path/to/project')
print(f"函数数: {result['summary']['total_functions']}")
print(f"类数: {result['summary']['total_classes']}")
```

### libcst分析

```python
from src.analyzers.libcst_analyzer import analyze_with_libcst

result = analyze_with_libcst('/path/to/file.py')
print(f"导入: {result['imports']}")
print(f"函数: {result['functions']}")
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

### 健康评分

```python
from src.analyzers.health_scorer import generate_health_report

metrics = {
    'total_commits': 6545,
    'contributors': 873,
    'avg_complexity': 1.41,
    'test_coverage': 50
}
report = generate_health_report(metrics)
print(f"评分: {report['score']}, 等级: {report['grade']}")
```

## 自定义分析

修改 `src/config.py` 配置：

```python
REPO_PATH = '../../your-repo'  # 目标仓库路径
DATA_DIR = 'data'              # 数据输出目录
OUTPUT_DIR = 'output'          # 图表输出目录
```
