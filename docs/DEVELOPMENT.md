# 开发说明

## 项目结构

```
src/
├── collectors/       # 数据采集模块
│   ├── git_collector.py     # Git历史采集
│   ├── github_api.py        # GitHub API
│   ├── branch_collector.py  # 分支信息
│   ├── tag_collector.py     # 标签信息
│   └── blame_collector.py   # Blame信息
├── analyzers/        # 分析模块
│   ├── ast_analyzer.py      # AST分析
│   ├── libcst_analyzer.py   # libcst分析
│   ├── stats.py             # 统计分析
│   └── quality_analyzer.py  # 质量分析
├── visualizers/      # 可视化模块
│   ├── charts.py            # 基础图表
│   ├── heatmap.py           # 热力图
│   └── trends.py            # 趋势图
└── utils/            # 工具模块
    ├── cache.py             # 缓存
    ├── logger.py            # 日志
    └── helpers.py           # 辅助函数
```

## 编码规范

- 遵循 PEP 8
- 使用类型注解
- 编写 docstring
- 中文注释可以

## 测试

```bash
pytest tests/ -v
```

## 贡献代码

1. Fork
2. 创建分支
3. 提交PR
