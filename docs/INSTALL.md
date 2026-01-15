# 安装指南

## 系统要求

- Python 3.8+
- Git
- 网络连接（用于GitHub API）

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 依赖说明

| 包名 | 用途 |
|------|------|
| pandas | 数据处理 |
| matplotlib | 图表绑定 |
| seaborn | 高级可视化 |
| wordcloud | 词云生成 |
| requests | HTTP请求 |
| libcst | 代码结构分析 |
| pysnooper | 动态追踪 |
| z3-solver | 符号执行 |

## 验证安装

```bash
python -c "from src.main import main; print('安装成功！')"
```

## 常见问题

### Q: matplotlib中文显示问题？
A: 项目已内置中文字体配置，无需额外设置。

### Q: z3-solver安装失败？
A: 尝试使用pip安装：`pip install z3-solver`

### Q: 如何更新依赖？
A: `pip install -r requirements.txt --upgrade`
