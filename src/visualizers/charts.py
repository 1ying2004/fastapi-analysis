"""
美化版图表模块
"""
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import os
from src.visualizers.font_config import configure_matplotlib, get_font_prop, FONT_PATH

configure_matplotlib()

def plot_commits_by_year(commits_data, output_dir='output'):
    """年度提交统计图 - 美化版"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits_data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    yearly = df.groupby('year').size()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(yearly)))
    bars = ax.bar(yearly.index.astype(str), yearly.values, color=colors, edgecolor='white', linewidth=1)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 20,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('年份', fontsize=14, fontweight='bold')
    ax.set_ylabel('提交数', fontsize=14, fontweight='bold')
    ax.set_title('FastAPI 年度提交统计', fontsize=18, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'commits_by_year.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 年度提交图: {output_dir}/commits_by_year.png")

def plot_author_pie(commits_data, output_dir='output', top_n=10):
    """作者贡献饼图 - 美化版"""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits_data)
    authors = df['author'].value_counts().head(top_n)
    other = df['author'].value_counts()[top_n:].sum()
    
    if other > 0:
        authors['其他'] = other
    
    fig, ax = plt.subplots(figsize=(12, 10))
    colors = plt.cm.Set3(np.linspace(0, 1, len(authors)))
    
    wedges, texts, autotexts = ax.pie(
        authors.values, 
        labels=authors.index, 
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        explode=[0.02] * len(authors),
        shadow=True,
        textprops={'fontsize': 10}
    )
    
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    ax.set_title('主要贡献者分布', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'authors_pie.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 作者饼图: {output_dir}/authors_pie.png")

def generate_wordcloud(text_data, output_dir='output'):
    """生成词云 - 美化版"""
    os.makedirs(output_dir, exist_ok=True)
    
    wc = WordCloud(
        font_path=FONT_PATH if FONT_PATH else None,
        width=1920,
        height=1080,
        background_color='white',
        colormap='viridis',
        max_words=300,
        min_font_size=8,
        max_font_size=150,
        random_state=42,
        contour_width=2,
        contour_color='steelblue'
    ).generate(text_data)
    
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('提交消息词云', fontsize=20, fontweight='bold', pad=20)
    
    plt.tight_layout(pad=0)
    plt.savefig(os.path.join(output_dir, 'wordcloud.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"✓ 词云: {output_dir}/wordcloud.png")
