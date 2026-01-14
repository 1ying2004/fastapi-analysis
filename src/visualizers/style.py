"""
样式配置
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import os

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

def setup_chinese():
    """配置中文字体"""
    if os.path.exists(FONT_PATH):
        fm.fontManager.addfont(FONT_PATH)
    
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['figure.dpi'] = 150

def apply_style(style='whitegrid'):
    """应用图表样式"""
    setup_chinese()
    sns.set_style(style)
    sns.set_palette("husl")
