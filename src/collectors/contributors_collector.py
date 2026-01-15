"""
Contributors采集模块 - 全量版

获取GitHub贡献者数据，支持增量持久化和实时热存储
"""
import requests
import json
import os
import time


class ContributorsCollector:
    """GitHub贡献者全量采集器"""
    
    def __init__(self, repo, token=None):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.contributors_file = os.path.join(self.data_dir, 'contributors.json')
    
    def _load_existing(self):
        """加载已有数据"""
        if os.path.exists(self.contributors_file):
            try:
                with open(self.contributors_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_realtime(self, data):
        """实时热存储"""
        with open(self.contributors_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def fetch_contributors(self):
        """获取全部贡献者"""
        existing = self._load_existing()
        existing_logins = {c.get('login') for c in existing if c.get('login')}
        
        all_contributors = list(existing)
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{self.repo}/contributors"
            params = {'page': page, 'per_page': 100, 'anon': 'true'}
            
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 403:
                    reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(reset_time - int(time.time()), 60)
                    print(f"  ⚠ API限流，等待{wait_time}秒...")
                    time.sleep(wait_time)
                    continue
                
                if resp.status_code != 200:
                    print(f"  ✗ 请求失败: {resp.status_code}")
                    break
                
                data = resp.json()
                if not data:
                    break
                
                for item in data:
                    login = item.get('login', 'Anonymous')
                    if login not in existing_logins:
                        contributor = {
                            'login': login,
                            'contributions': item['contributions'],
                            'type': item.get('type', 'Anonymous'),
                            'avatar_url': item.get('avatar_url', ''),
                            'html_url': item.get('html_url', '')
                        }
                        all_contributors.append(contributor)
                        existing_logins.add(login)
                
                self._save_realtime(all_contributors)
                
                print(f"  获取第{page}页，累计{len(all_contributors)}位贡献者")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ 错误: {e}")
                break
        
        return all_contributors
    
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
        top10 = sorted(contributors, key=lambda x: -x['contributions'])[:10]
        
        return {
            'total_contributors': len(contributors),
            'total_contributions': total,
            'avg_contributions': total / len(contributors),
            'top10': [(c['login'], c['contributions']) for c in top10]
        }
