"""
constants常量定义
"""

COMMIT_TYPES = {
    'feat': '新功能',
    'fix': '修复',
    'docs': '文档',
    'refactor': '重构',
    'test': '测试',
    'chore': '杂项',
    'style': '样式',
    'perf': '性能'
}

CHART_COLORS = [
    '#667eea', '#764ba2', '#48bb78', '#ed8936',
    '#f56565', '#9f7aea', '#38b2ac', '#a0aec0'
]

FILE_EXTENSIONS_MAP = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript', 
    '.md': 'Markdown',
    '.json': 'JSON',
    '.yml': 'YAML',
    '.yaml': 'YAML',
    '.html': 'HTML',
    '.css': 'CSS',
    '.sql': 'SQL'
}

DEFAULT_MAX_COMMITS = 10000
DEFAULT_DPI = 150
