# FastAPI 仓库深度分析工具

[![CI](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml)

使用 **ast** | **libcst** | **pysnooper** | **z3-solver** 对 FastAPI 开源项目进行深度分析。

## 🎯 项目特点

- 📊 全量采集 6,545+ 条 Git 提交历史
- 🔍 AST 静态分析：函数、类、复杂度、依赖
- 🧪 libcst 高级代码结构分析
- 🐛 pysnooper 动态追踪
- 🔐 z3-solver 符号执行
- 📈 15+ 张精美可视化图表
- 🇨🇳 完美中文支持
- ✅ 完整测试覆盖

## 🚀 快速开始

```bash
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis
pip install -r requirements.txt
python src/main.py
```

## 📁 项目结构

```
src/
├── collectors/          # 数据采集模块
│   ├── git_collector.py       # Git历史采集
│   ├── github_api.py          # GitHub API
│   ├── issues_collector.py    # Issues/PR采集
│   └── contributors_collector.py
├── analyzers/           # 代码分析模块
│   ├── ast_analyzer.py        # AST深度分析 (ast)
│   ├── libcst_analyzer.py     # 代码结构 (libcst)
│   ├── dynamic_tracer.py      # 动态追踪 (pysnooper)
│   ├── z3_analysis.py         # 符号执行 (z3-solver)
│   ├── dependency_analyzer.py # 依赖分析
│   ├── health_scorer.py       # 健康评分
│   └── ...
├── visualizers/         # 可视化模块
│   ├── charts.py              # 基础图表
│   ├── heatmap.py             # 热力图
│   ├── trends.py              # 趋势图
│   └── ...
└── utils/               # 工具模块
```

## 📊 分析结果

| 指标 | 数值 |
|------|------|
| 总提交数 | 6,545 |
| 贡献者数 | 873 |
| Python文件 | 1,252 |
| 函数数 | 4,636 |
| 类数 | 827 |
| 代码行数 | 90,708 |

## 📈 生成的图表

- 年度提交统计图
- 主要贡献者饼图
- Top15 作者排行
- 提交时间热力图
- 月度趋势曲线
- 累计增长曲线
- 文件类型分布
- 代码行数对比
- 函数复杂度分布
- 依赖频率分析
- 提交类型分析
- 词云

## 🛠️ 技术栈

- **ast**: Python标准库，AST静态分析
- **libcst**: 具体语法树，高级代码分析
- **pysnooper**: 动态追踪调试
- **z3-solver**: SMT求解器，符号执行
- **matplotlib/seaborn**: 数据可视化
- **pandas**: 数据处理

## 👥 团队

5人协作开发

## 📄 许可

MIT License
