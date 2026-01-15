# FastAPI 仓库深度分析工具

[![CI](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml)

使用 **ast** | **libcst** | **pysnooper** | **z3-solver** 对 FastAPI 开源项目进行深度分析。

## 🎯 项目特点

- 📊 全量采集 6,545+ 条 Git 提交历史
- 📋 GitHub Issues、Pull Requests、Contributors 采集
- 🔍 AST 静态分析：函数、类、复杂度、依赖
- 🧪 libcst 高级代码结构分析
- 🐛 pysnooper 动态追踪
- 🔐 z3-solver 符号执行
- 📈 25+ 张精美可视化图表（含3D）
- 🇨🇳 完美中文支持

## 🚀 快速开始

```bash
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis
pip install -r requirements.txt

# 完整分析（使用缓存数据，跳过长时间限流）
python src/main.py

# 仅获取全量数据（完整等待API限流）
python src/main.py --fetch
```

## 📋 运行模式

### 默认模式
```bash
python src/main.py
```
- 快速分析，使用已缓存的GitHub数据
- 遇到API限流>2分钟自动跳过
- 完成全部图表生成

### 数据获取模式
```bash
python src/main.py --fetch
```
- 专门获取全量GitHub数据
- 完整等待API限流（无超时）
- 适合首次运行或更新数据

## 📁 输出目录

```
data/                        # 采集的原始数据
├── commits.csv/json         # 提交记录
├── issues.json              # GitHub Issues
├── pull_requests.json       # GitHub PRs
├── contributors.json        # 贡献者数据
├── ast_analysis.json        # AST分析结果
├── report.json              # 统计报告
└── loc_stats.json           # 代码行数

output/                      # 可视化结果
├── commits_by_year.png      # 年度提交
├── commit_heatmap.png       # 热力图
├── commits_3d.png           # 3D年月分布
├── author_3d.png            # 3D作者活跃
├── ...                      # 共25+张图表
└── summary.json             # 摘要数据
```

## 📊 生成的图表

| 类别 | 图表 |
|------|------|
| 提交分析 | 年度统计、月度趋势、累计增长、热力图、词云 |
| 作者分析 | 贡献饼图、Top15排行、3D活跃度 |
| 代码分析 | 文件类型、代码行数、复杂度分布、函数数量 |
| 3D图表 | 年月提交分布、作者活跃度 |
| Issues/PR | 状态分布、时间线、Top创建者 |
| 依赖分析 | 导入频率、文件依赖 |

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **ast** | Python AST静态分析 |
| **libcst** | 具体语法树分析 |
| **pysnooper** | 动态追踪调试 |
| **z3-solver** | SMT求解器/符号执行 |
| **matplotlib/seaborn** | 数据可视化 |
| **pandas** | 数据处理 |

## 🔧 配置

编辑 `src/config.py`：

```python
REPO_PATH = '../../fastapi'      # 目标Git仓库
GITHUB_REPO = 'tiangolo/fastapi' # GitHub仓库名
```
