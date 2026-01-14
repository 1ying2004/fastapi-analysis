# 贡献指南

## 如何贡献

1. Fork本仓库
2. 创建特性分支 `git checkout -b feature/xxx`
3. 提交改动 `git commit -m "feat: xxx"`
4. 推送 `git push origin feature/xxx` 
5. 创建Pull Request

## 代码规范

- 使用Python 3.8+语法
- 遵循PEP 8
- 添加类型注解
- 编写测试用例

## 提交消息格式

```
<type>: <subject>

类型:
- feat: 新功能
- fix: 修复
- docs: 文档
- refactor: 重构
- test: 测试
- chore: 杂项
```

## 测试

```bash
pip install -r requirements-dev.txt
pytest
```
