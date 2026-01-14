import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import os

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"

def setup_fonts():
    """配置中文字体"""
    if os.path.exists(FONT_PATH):
        fm.fontManager.addfont(FONT_PATH)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    sns.set_style("whitegrid")

def plot_commits_by_year(commits_data, output_dir='output'):
    """年度提交统计图"""
    setup_fonts()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits_data)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    yearly = df.groupby('year').size()
    
    plt.figure(figsize=(14, 7))
    bars = plt.bar(yearly.index.astype(str), yearly.values, color='#667eea', alpha=0.8)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                f'{int(height)}', ha='center', va='bottom', fontsize=11)
    
    plt.xlabel('年份', fontsize=14, fontweight='bold')
    plt.ylabel('提交数', fontsize=14, fontweight='bold')
    plt.title('年度提交统计图', fontsize=18, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'commits_by_year.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存: {output_dir}/commits_by_year.png")

def plot_author_pie(commits_data, output_dir='output'):
    """作者贡献饼图"""
    setup_fonts()
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(commits_data)
    authors = df['author'].value_counts().head(10)
    
    plt.figure(figsize=(12, 8))
    colors = sns.color_palette('husl', len(authors))
    plt.pie(authors.values, labels=authors.index, autopct='%1.1f%%',
            colors=colors, startangle=90)
    plt.title('主要贡献者分布', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'authors_pie.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存: {output_dir}/authors_pie.png")

def generate_wordcloud(text_data, output_dir='output'):
    """生成词云"""
    setup_fonts()
    os.makedirs(output_dir, exist_ok=True)
    
    wc = WordCloud(
        font_path=FONT_PATH if os.path.exists(FONT_PATH) else None,
        width=1600,
        height=800,
        background_color='white',
        colormap='viridis',
        max_words=200
    ).generate(text_data)
    
    plt.figure(figsize=(16, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('提交消息词云', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout(pad=0)
    plt.savefig(os.path.join(output_dir, 'wordcloud.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ 已保存: {output_dir}/wordcloud.png")
