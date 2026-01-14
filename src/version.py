"""
版本信息
"""
__version__ = '0.2.0'
__author__ = 'FastAPI Analysis Team'
__email__ = '2587586776@qq.com'
__description__ = 'FastAPI 仓库深度分析工具'

VERSION_INFO = {
    'major': 0,
    'minor': 2,
    'patch': 0,
    'release': 'stable'
}

def get_version():
    return __version__

def get_version_info():
    return VERSION_INFO
