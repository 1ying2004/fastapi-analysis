# FastAPI Analysis

深度分析FastAPI开源仓库。

## 功能

- **Git历史分析**: 完整commit历史分析
- **代码结构分析**: AST/libcst代码扫描  
- **数据可视化**: matplotlib/seaborn图表
- **GitHub API**: Issues/PRs数据采集

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
python src/main.py
```

## 项目结构

```
src/
  ├── collectors/    # 数据采集
  ├── analyzers/     # 代码分析
  ├── visualizers/   # 可视化
  └── utils/         # 工具函数
```
