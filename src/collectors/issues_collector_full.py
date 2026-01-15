"""
Issues全量采集模块

特性：
- 分别获取open和closed状态
- 指数退避等待（适合切换代理）
- 断点续传（记录页码）
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
        
        self.progress_file = os.path.join(self.data_dir, '.fetch_progress.json')
    
    def _load_progress(self):
        """加载进度"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_progress(self, key, page):
        """保存进度"""
        progress = self._load_progress()
        progress[key] = page
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f)
    
    def _exponential_backoff(self, attempt, base=30, max_wait=300):
        """指数退避等待"""
        wait = min(base * (2 ** attempt), max_wait)
        print(f"    ⏳ 等待{wait}秒后重试 (尝试{attempt+1})...")
        time.sleep(wait)
    
    def _load_existing_issues(self):
        """加载已有issues"""
        filepath = os.path.join(self.data_dir, 'issues.json')
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_issues(self, issues):
        """保存issues"""
        filepath = os.path.join(self.data_dir, 'issues.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
    
    def fetch_all_issues(self):
        """获取全部Issues（open + closed）"""
        existing = self._load_existing_issues()
        existing_numbers = {i['number'] for i in existing}
        all_issues = list(existing)
        
        progress = self._load_progress()
        
        for state in ['open', 'closed']:
            progress_key = f'issues_{state}'
            start_page = progress.get(progress_key, 1)
            page = start_page
            retry_count = 0
            
            print(f"    获取{state}状态issues (从第{start_page}页开始)...")
            
            while True:
                url = f"{self.base_url}/repos/{self.repo}/issues"
                params = {'state': state, 'page': page, 'per_page': 100, 'sort': 'created', 'direction': 'asc'}
                
                try:
                    resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                    
                    if resp.status_code == 403:
                        retry_count += 1
                        if retry_count > 10:
                            print(f"    ❌ 重试次数过多，跳过")
                            break
                        self._exponential_backoff(retry_count)
                        continue
                    
                    if resp.status_code != 200:
                        print(f"    ❌ 请求失败: {resp.status_code}")
                        break
                    
                    data = resp.json()
                    if not data:
                        break
                    
                    retry_count = 0
                    new_count = 0
                    
                    for item in data:
                        if 'pull_request' in item:
                            continue
                        if item['number'] not in existing_numbers:
                            all_issues.append({
                                'number': item['number'],
                                'title': item['title'],
                                'state': item['state'],
                                'author': item['user']['login'],
                                'created_at': item['created_at'],
                                'closed_at': item.get('closed_at'),
                                'labels': [l['name'] for l in item.get('labels', [])]
                            })
                            existing_numbers.add(item['number'])
                            new_count += 1
                    
                    self._save_issues(all_issues)
                    self._save_progress(progress_key, page + 1)
                    
                    total_state = len([i for i in all_issues if i['state'] == state])
                    print(f"    第{page}页 (+{new_count}), {state}总计{total_state}条")
                    
                    if len(data) < 100:
                        break
                    
                    page += 1
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"    ⚠ 错误: {e}")
                    retry_count += 1
                    if retry_count > 5:
                        break
                    self._exponential_backoff(retry_count)
            
            self._save_progress(progress_key, 1)
        
        print(f"  ✓ Issues总计: {len(all_issues)} (open: {len([i for i in all_issues if i['state']=='open'])}, closed: {len([i for i in all_issues if i['state']=='closed'])})")
        return all_issues
    
    def fetch_all_prs(self):
        """获取全部PRs"""
        filepath = os.path.join(self.data_dir, 'pull_requests.json')
        existing = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except:
                pass
        
        existing_numbers = {p['number'] for p in existing}
        all_prs = list(existing)
        
        progress = self._load_progress()
        
        for state in ['open', 'closed']:
            progress_key = f'prs_{state}'
            start_page = progress.get(progress_key, 1)
            page = start_page
            retry_count = 0
            
            print(f"    获取{state}状态PRs (从第{start_page}页开始)...")
            
            while True:
                url = f"{self.base_url}/repos/{self.repo}/pulls"
                params = {'state': state, 'page': page, 'per_page': 100, 'sort': 'created', 'direction': 'asc'}
                
                try:
                    resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                    
                    if resp.status_code == 403:
                        retry_count += 1
                        if retry_count > 10:
                            break
                        self._exponential_backoff(retry_count)
                        continue
                    
                    if resp.status_code != 200:
                        break
                    
                    data = resp.json()
                    if not data:
                        break
                    
                    retry_count = 0
                    
                    for item in data:
                        if item['number'] not in existing_numbers:
                            all_prs.append({
                                'number': item['number'],
                                'title': item['title'],
                                'state': item['state'],
                                'author': item['user']['login'],
                                'created_at': item['created_at'],
                                'merged_at': item.get('merged_at')
                            })
                            existing_numbers.add(item['number'])
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(all_prs, f, ensure_ascii=False, indent=2)
                    self._save_progress(progress_key, page + 1)
                    
                    print(f"    第{page}页，{state}累计{len([p for p in all_prs if p['state']==state])}条")
                    
                    if len(data) < 100:
                        break
                    
                    page += 1
                    time.sleep(1)
                    
                except Exception as e:
                    retry_count += 1
                    if retry_count > 5:
                        break
                    self._exponential_backoff(retry_count)
            
            self._save_progress(progress_key, 1)
        
        print(f"  ✓ PRs总计: {len(all_prs)}")
        return all_prs
