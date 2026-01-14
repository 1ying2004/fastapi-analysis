"""
全局字体配置 - 确保中文完美显示
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import os
import warnings

warnings.filterwarnings('ignore', category=UserWarning)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]

FONT_PATH = None
FONT_PROP = None

def find_chinese_font():
    """查找可用中文字体"""
    global FONT_PATH, FONT_PROP
    
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            FONT_PATH = path
            fm.fontManager.addfont(path)
            FONT_PROP = fm.FontProperties(fname=path)
            return path
    
    return None

def configure_matplotlib():
    """配置matplotlib全局中文支持"""
    find_chinese_font()
    
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'Arial Unicode MS', 'DejaVu Sans']
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['figure.dpi'] = 150
    matplotlib.rcParams['savefig.dpi'] = 150
    matplotlib.rcParams['figure.facecolor'] = 'white'
    matplotlib.rcParams['axes.facecolor'] = 'white'
    matplotlib.rcParams['font.size'] = 12
    
    if FONT_PATH:
        matplotlib.rcParams['font.family'] = 'sans-serif'

def get_font_prop():
    """获取字体属性对象"""
    if FONT_PROP is None:
        find_chinese_font()
    return FONT_PROP

configure_matplotlib()
