"""
Contributors全量采集模块

无超时限制
"""
import requests
import json
import os
import time


class ContributorsCollectorFull:
    """全量贡献者采集器"""
    
    def __init__(self, repo, token=None):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_all(self):
        """获取全部贡献者"""
        contributors = []
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{self.repo}/contributors"
            params = {'page': page, 'per_page': 100, 'anon': 'true'}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 403:
                    reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(reset_time - int(time.time()), 60)
                    print(f"    ⏳ API限流，等待{wait_time}秒...")
                    time.sleep(wait_time)
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
                        'type': item.get('type', 'Anonymous')
                    })
                
                print(f"    第{page}页，累计{len(contributors)}位")
                
                if len(data) < 100:
                    break
                page += 1
                time.sleep(1)
                
            except Exception as e:
                print(f"    错误: {e}")
                time.sleep(5)
        
        filepath = os.path.join(self.data_dir, 'contributors.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(contributors, f, ensure_ascii=False, indent=2)
        
        return contributors
