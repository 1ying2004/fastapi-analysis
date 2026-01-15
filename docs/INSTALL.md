# 安装指南

## 系统要求

- Python 3.8+ (推荐3.10+)
- Git 2.0+
- 网络连接（用于GitHub API）
- Windows/Linux/macOS

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis
```

### 2. 克隆目标仓库

本项目分析FastAPI仓库，需要先克隆：

```bash
cd ..
git clone https://github.com/tiangolo/fastapi.git
cd fastapi-analysis
```

### 3. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

## 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| pandas | >=1.5.0 | 数据处理与分析 |
| matplotlib | >=3.6.0 | 基础图表绑定 |
| seaborn | >=0.12.0 | 高级统计可视化 |
| wordcloud | >=1.8.0 | 词云生成 |
| requests | >=2.28.0 | GitHub API请求 |
| libcst | >=0.4.0 | 具体语法树分析 |
| pysnooper | >=1.1.0 | 动态追踪调试 |
| z3-solver | >=4.12.0 | SMT求解/符号执行 |
| pytest | >=7.0.0 | 单元测试框架 |

## 验证安装

```bash
# 验证导入
python -c "from src.main import main; print('安装成功！')"

# 运行测试
python -m pytest tests/ -v
```

## 常见问题

### Q: matplotlib中文显示问题？
A: 项目已内置中文字体配置（font_config.py），自动检测系统中文字体，无需额外设置。

### Q: z3-solver安装失败？
A: Windows用户尝试：`pip install z3-solver`；Linux用户可能需要先安装z3：`sudo apt install z3`

### Q: libcst安装报错？
A: 需要Python 3.8+，尝试升级pip：`pip install --upgrade pip`

### Q: GitHub API限流？
A: 可以在src/config.py中配置GITHUB_TOKEN以提高限制。

### Q: 如何更新依赖？
A: `pip install -r requirements.txt --upgrade`
