# 安装说明

## 环境要求

- Python 3.8 或更高版本
- Git
- Windows/Linux/macOS

## 安装步骤

```bash
# 克隆仓库
git clone https://github.com/1ying2004/fastapi-analysis.git
cd fastapi-analysis

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

## 验证安装

```bash
python -c "from src.collectors import git_collector; print('OK')"
python src/main.py
```

## 常见问题

### 中文字体问题

确保系统安装了微软雅黑字体，或修改 `src/config.py` 中的 `FONT_PATH`。

### z3-solver 安装慢

```bash
pip install z3-solver --timeout 300
```
