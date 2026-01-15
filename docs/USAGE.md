# 使用指南

## 运行模式

### 1. 完整分析模式（默认）

```bash
python src/main.py
```

执行流程：
1. Git数据采集 - 获取全部提交历史
2. GitHub数据采集 - 使用缓存，限流>2分钟跳过
3. AST代码分析 - 分析所有Python文件
4. 统计分析 - 生成报告
5. 生成图表 - 25+张可视化图表

### 2. 数据获取模式

```bash
python src/main.py --fetch
```

专门用于获取全量GitHub数据：
- 完整等待API限流（无超时）
- 适合首次运行或数据更新
- 获取全部Issues、PRs、Contributors

## 输出说明

### 数据文件 (data/)

| 文件 | 内容 |
|------|------|
| commits.csv/json | Git提交记录 |
| issues.json | GitHub Issues |
| pull_requests.json | Pull Requests |
| contributors.json | 贡献者 |
| ast_analysis.json | AST分析结果 |
| report.json | 统计报告 |
| loc_stats.json | 代码行数 |
| message_stats.json | 消息类型 |

### 图表文件 (output/)

共25+张PNG图表，包括：
- 年度/月度提交统计
- 作者贡献分析
- 3D可视化
- Issues/PR分析
- 代码复杂度
- 依赖关系
- 词云

## 自定义配置

编辑 `src/config.py`：

```python
REPO_PATH = '../../your-repo'      # 目标仓库路径
GITHUB_REPO = 'owner/repo'         # GitHub仓库名
GITHUB_TOKEN = 'your_token'        # 可选，提高API限制
```

## 常见问题

### Q: API限流怎么办？
A: 默认模式会跳过长时间限流，使用`--fetch`模式完整等待

### Q: 图表中文乱码？
A: 已内置中文字体配置，无需额外设置

### Q: 如何更新数据？
A: 删除data/目录下对应JSON文件，重新运行
