"""
异常定义
"""

class AnalysisError(Exception):
    """分析错误基类"""
    pass

class CollectorError(AnalysisError):
    """数据采集错误"""
    pass

class GitError(CollectorError):
    """Git操作错误"""
    pass

class APIError(CollectorError):
    """API调用错误"""
    pass

class RateLimitError(APIError):
    """API限流错误"""
    pass

class VisualizationError(AnalysisError):
    """可视化错误"""
    pass

class ConfigError(AnalysisError):
    """配置错误"""
    pass
