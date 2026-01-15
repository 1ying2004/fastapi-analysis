"""
Contributors采集模块

获取GitHub贡献者数据
"""
import requests
import json
import os
import time


class ContributorsCollector:
    """GitHub贡献者采集器"""
    
    def __init__(self, repo, token=None):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_contributors(self, max_pages=9999):
        """
        获取贡献者列表
        
        Returns:
            贡献者列表
        """
        contributors = []
        page = 1
        
        while page <= max_pages:
            url = f"{self.base_url}/repos/{self.repo}/contributors"
            params = {'page': page, 'per_page': 100, 'anon': 'true'}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 403:
                    print("  ⚠ API限流，等待60秒...")
                    time.sleep(60)
                    continue
                
                if resp.status_code != 200:
                    break
                
                data = resp.json()
                if not data:
                    break
                
                for item in data:
                    contributors.append({
                        'login': item.get('login', 'Anonymous'),
                        'contributions': item['contributions'],
                        'type': item.get('type', 'Anonymous'),
                        'avatar_url': item.get('avatar_url', '')
                    })
                
                print(f"  获取第{page}页，累计{len(contributors)}位贡献者")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ 错误: {e}")
                break
        
        return contributors
    
    def save_contributors(self, contributors, filename='contributors.json'):
        """保存贡献者数据"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(contributors, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(contributors)}位)")
    
    def get_stats(self, contributors):
        """生成贡献者统计"""
        if not contributors:
            return {}
        
        total = sum(c['contributions'] for c in contributors)
        top10 = contributors[:10]
        
        return {
            'total_contributors': len(contributors),
            'total_contributions': total,
            'avg_contributions': total / len(contributors),
            'top10': [(c['login'], c['contributions']) for c in top10]
        }
