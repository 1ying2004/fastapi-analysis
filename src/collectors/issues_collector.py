"""
Issues采集模块

获取GitHub Issues和Pull Requests数据
"""
import requests
import json
import os
import time

class IssuesCollector:
    """GitHub Issues采集器"""
    
    def __init__(self, repo, token=None):
        """
        初始化采集器
        
        Args:
            repo: 仓库名 owner/repo
            token: GitHub Token (可选)
        """
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_issues(self, state='all', max_pages=50):
        """
        获取issues（不含PR）
        
        Args:
            state: 状态 all/open/closed
            max_pages: 最大页数
        
        Returns:
            issues列表
        """
        issues = []
        page = 1
        
        while page <= max_pages:
            url = f"{self.base_url}/repos/{self.repo}/issues"
            params = {'state': state, 'page': page, 'per_page': 100}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 403:
                    print("  ⚠ API限流，等待60秒...")
                    time.sleep(60)
                    continue
                
                if resp.status_code != 200:
                    print(f"  ✗ 请求失败: {resp.status_code}")
                    break
                
                data = resp.json()
                if not data:
                    break
                
                for item in data:
                    if 'pull_request' not in item:
                        issues.append({
                            'number': item['number'],
                            'title': item['title'],
                            'state': item['state'],
                            'author': item['user']['login'],
                            'created_at': item['created_at'],
                            'labels': [l['name'] for l in item['labels']]
                        })
                
                print(f"  获取第{page}页，累计{len(issues)}个issues")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ 错误: {e}")
                break
        
        return issues
    
    def fetch_pull_requests(self, state='all', max_pages=50):
        """
        获取Pull Requests
        """
        prs = []
        page = 1
        
        while page <= max_pages:
            url = f"{self.base_url}/repos/{self.repo}/pulls"
            params = {'state': state, 'page': page, 'per_page': 100}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code != 200:
                    break
                
                data = resp.json()
                if not data:
                    break
                
                for item in data:
                    prs.append({
                        'number': item['number'],
                        'title': item['title'],
                        'state': item['state'],
                        'author': item['user']['login'],
                        'created_at': item['created_at'],
                        'merged': item.get('merged_at') is not None
                    })
                
                print(f"  获取第{page}页，累计{len(prs)}个PRs")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ 错误: {e}")
                break
        
        return prs
    
    def save_issues(self, issues, filename='issues.json'):
        """保存issues到JSON"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(issues)}条)")
    
    def save_prs(self, prs, filename='pull_requests.json'):
        """保存PRs到JSON"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(prs, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(prs)}条)")
