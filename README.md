# FastAPI 仓库深度分析工具

[![CI](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml)

使用 **ast** | **libcst** | **pysnooper** | **z3-solver** 对 FastAPI 开源项目进行深度分析。

## 🎯 项目特点

- 📊 全量采集 6,545+ 条 Git 提交历史
- 🔍 AST 静态分析：函数、类、复杂度
- 🧪 libcst 高级代码结构分析
- 🐛 pysnooper 动态追踪
- 🔐 z3-solver 符号执行
- 📈 10+ 张精美可视化图表
- 🇨🇳 完美中文支持

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis

# 安装依赖
pip install -r requirements.txt

# 运行分析
python src/main.py
```

## 📁 项目结构

```
src/
├── collectors/     # 数据采集模块
│   ├── git_collector.py      # Git历史采集
│   ├── github_api.py         # GitHub API
│   ├── branch_collector.py   # 分支信息
│   └── tag_collector.py      # 标签信息
├── analyzers/      # 代码分析模块
│   ├── ast_analyzer.py       # AST深度分析
│   ├── libcst_analyzer.py    # libcst分析
│   ├── dynamic_tracer.py     # pysnooper追踪
│   ├── z3_analysis.py        # z3符号执行
│   └── stats.py              # 统计分析
├── visualizers/    # 可视化模块
│   ├── charts.py             # 基础图表
│   ├── heatmap.py            # 热力图
│   ├── trends.py             # 趋势图
│   └── complexity_charts.py  # 复杂度图表
└── utils/          # 工具模块
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
- 文件类型分布
- 代码行数对比
- 函数复杂度分布
- 词云

## 👥 团队

5人协作开发

## 📄 许可

MIT License
