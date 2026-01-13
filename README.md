# FastAPI Analysis

FastAPI 开源仓库深度分析工具。

## 功能

- **数据采集**: Git历史 + GitHub API
- **代码分析**: AST/libcst静态分析 + pysnooper动态追踪 + z3符号执行
- **可视化**: matplotlib/seaborn图表 + 词云

## 快速开始

```bash
# 安装
pip install -r requirements.txt

# 运行
python src/main.py
```

## 项目结构

```
src/
├── collectors/     # 数据采集
│   ├── git_collector.py
│   └── github_api.py
├── analyzers/      # 代码分析
│   ├── ast_analyzer.py
│   ├── libcst_analyzer.py
│   ├── dynamic_tracer.py
│   └── z3_analysis.py
├── visualizers/    # 可视化
│   ├── charts.py
│   └── heatmap.py
└── utils/          # 工具
    ├── helpers.py
    └── cache.py
```

## 输出

- `data/commits.csv` - 提交数据
- `data/commits.json` - JSON格式数据
- `output/*.png` - 可视化图表

## 团队

5人协作开发
