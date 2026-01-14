# FastAPI Analysis

FastAPI 仓库深度分析工具。

[![CI](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml)

## 功能

- **数据采集**: Git历史 + GitHub API
- **代码分析**: AST/libcst静态分析 + pysnooper动态追踪 + z3符号执行
- **可视化**: matplotlib/seaborn图表 + 词云

## 快速开始

```bash
pip install -r requirements.txt
python src/main.py
```

## 项目结构

```
src/
├── collectors/     # 数据采集
├── analyzers/      # 代码分析
├── visualizers/    # 可视化
└── utils/          # 工具
```

## 输出

- `data/commits.csv` - 提交数据
- `data/commits.json` - JSON格式数据
- `output/*.png` - 可视化图表

## 团队

5人协作开发
