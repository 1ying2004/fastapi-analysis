import requests
import time
import json
import os

class GitHubAPI:
    """GitHub API客户端"""
    
    def __init__(self, repo, token=None):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def _fetch_paginated(self, url, params, max_items=5000):
        """分页获取数据"""
        all_items = []
        page = 1
        
        while len(all_items) < max_items:
            params['page'] = page
            params['per_page'] = 100
            
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 403:
                print("API限流，等待60秒...")
                time.sleep(60)
                continue
            
            if response.status_code != 200:
                print(f"请求失败: {response.status_code}")
                break
            
            items = response.json()
            if not items:
                break
            
            all_items.extend(items)
            print(f"  已获取 {len(all_items)} 条...")
            page += 1
            time.sleep(0.3)
        
        return all_items
    
    def get_issues(self, state='all'):
        """获取issues"""
        url = f"{self.base_url}/repos/{self.repo}/issues"
        return self._fetch_paginated(url, {'state': state})
    
    def get_contributors(self):
        """获取贡献者"""
        url = f"{self.base_url}/repos/{self.repo}/contributors"
        return self._fetch_paginated(url, {})
    
    def save_data(self, data, filename, output_dir='data'):
        os.makedirs(output_dir, exist_ok=True)
        filepath = f"{output_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath}")
