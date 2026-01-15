# FastAPI 仓库深度分析工具

[![CI](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/1ying2004/fastapi-analysis/actions/workflows/ci.yml)

使用 **ast** | **libcst** | **pysnooper** | **z3-solver** 对 FastAPI 开源项目进行深度分析。

## 🎯 项目特点

- 📊 全量采集 6,545+ 条 Git 提交历史
- � 全量采集 GitHub Issues、Pull Requests、Contributors
- �🔍 AST 静态分析：函数、类、复杂度、依赖
- 🧪 libcst 高级代码结构分析
- 🐛 pysnooper 动态追踪
- 🔐 z3-solver 符号执行
- 📈 18+ 张精美可视化图表
- 🇨🇳 完美中文支持
- ✅ 完整测试覆盖

## 🚀 快速开始

```bash
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis
pip install -r requirements.txt
python src/main.py
```

## � 完整分析流程

运行 `python src/main.py` 后，工具会依次执行：

### 1️⃣ Git数据采集
- 获取全部 6,545+ 条提交历史
- 获取分支、标签信息
- 保存为 CSV 和 JSON 格式

### 2️⃣ GitHub API采集
- 全量获取 Issues（区分真实issue和PR）
- 全量获取 Pull Requests
- 全量获取所有贡献者信息

### 3️⃣ AST代码分析
- 使用 `ast` 模块解析所有Python文件
- 提取函数、类、导入信息
- 计算圈复杂度

### 4️⃣ 统计分析
- 作者贡献统计
- 提交时间分布
- 消息类型分类
- 代码行数统计
- 依赖关系分析

### 5️⃣ 项目健康评分
- 综合评估项目质量
- 生成健康度评分 (0-100)
- 给出改进建议

### 6️⃣ 生成可视化图表
| 图表 | 说明 |
|------|------|
| commits_by_year.png | 年度提交统计 |
| authors_pie.png | 贡献者分布饼图 |
| top_authors.png | Top15作者排行 |
| commit_heatmap.png | 提交时间热力图 |
| monthly_trend.png | 月度趋势曲线 |
| cumulative.png | 累计增长曲线 |
| file_types.png | 文件类型分布 |
| loc_bar.png | 代码行数对比 |
| complexity_dist.png | 函数复杂度分布 |
| function_count.png | 文件函数数量排行 |
| commit_types.png | 提交类型分析 |
| yearly_comparison.png | 年度对比图 |
| import_frequency.png | 导入频率分析 |
| file_dependencies.png | 文件依赖分析 |
| issues_state.png | Issues状态分布 |
| issues_timeline.png | Issues创建时间线 |
| top_contributors.png | Top贡献者排行 |
| contributions_dist.png | 贡献分布直方图 |
| wordcloud.png | 提交消息词云 |

### 7️⃣ 生成报告
- HTML可视化报告
- JSON摘要数据

## 📁 输出目录

```
data/                        # 采集的原始数据
├── commits.csv              # 提交记录
├── commits.json             
├── issues.json              # GitHub Issues
├── pull_requests.json       # GitHub PRs
├── contributors.json        # 贡献者数据
├── ast_analysis.json        # AST分析结果
├── report.json              # 统计报告
├── loc_stats.json           # 代码行数
├── message_stats.json       # 消息类型
└── health_report.json       # 健康评分

output/                      # 可视化结果
├── *.png                    # 18+张图表
├── report.html              # HTML报告
└── summary.json             # 摘要数据
```

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **ast** | Python标准库，AST静态分析 |
| **libcst** | 具体语法树，高级代码分析 |
| **pysnooper** | 动态追踪调试 |
| **z3-solver** | SMT求解器，符号执行 |
| **matplotlib/seaborn** | 数据可视化 |
| **pandas** | 数据处理 |
| **requests** | GitHub API调用 |
| **wordcloud** | 词云生成 |

## 📊 分析结果示例

| 指标 | 数值 |
|------|------|
| 总提交数 | 6,545 |
| 贡献者数 | 873 |
| Python文件 | 1,252 |
| 函数数 | 4,636 |
| 类数 | 827 |
| 代码行数 | 90,708 |

## � 配置

编辑 `src/config.py` 自定义分析目标：

```python
REPO_PATH = '../../fastapi'      # 目标Git仓库路径
GITHUB_REPO = 'tiangolo/fastapi' # GitHub仓库名
DATA_DIR = 'data'                # 数据输出目录
OUTPUT_DIR = 'output'            # 图表输出目录
```
