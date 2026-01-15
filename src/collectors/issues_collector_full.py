"""
Issues全量采集模块

无超时限制，完整等待API限流
"""
import requests
import json
import os
import time


class IssuesCollectorFull:
    """全量Issues采集器"""
    
    def __init__(self, repo, token=None):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _wait_for_rate_limit(self, resp):
        """等待限流"""
        reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
        wait_time = max(reset_time - int(time.time()), 60)
        print(f"    ⏳ API限流，等待{wait_time}秒...")
        time.sleep(wait_time)
    
    def fetch_all_issues(self):
        """获取全部Issues"""
        issues = []
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{self.repo}/issues"
            params = {'state': 'all', 'page': page, 'per_page': 100}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 403:
                    self._wait_for_rate_limit(resp)
                    continue
                
                if resp.status_code != 200:
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
                            'created_at': item['created_at']
                        })
                
                print(f"    第{page}页，累计{len(issues)}条issues")
                
                if len(data) < 100:
                    break
                page += 1
                time.sleep(1)
                
            except Exception as e:
                print(f"    错误: {e}")
                time.sleep(5)
        
        filepath = os.path.join(self.data_dir, 'issues.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        
        return issues
    
    def fetch_all_prs(self):
        """获取全部PRs"""
        prs = []
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{self.repo}/pulls"
            params = {'state': 'all', 'page': page, 'per_page': 100}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 403:
                    self._wait_for_rate_limit(resp)
                    continue
                
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
                        'merged_at': item.get('merged_at')
                    })
                
                print(f"    第{page}页，累计{len(prs)}条PRs")
                
                if len(data) < 100:
                    break
                page += 1
                time.sleep(1)
                
            except Exception as e:
                print(f"    错误: {e}")
                time.sleep(5)
        
        filepath = os.path.join(self.data_dir, 'pull_requests.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(prs, f, ensure_ascii=False, indent=2)
        
        return prs
