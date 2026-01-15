"""
Issues采集模块 - 全量版

使用GitHub Search API获取全部Issues和Pull Requests
支持增量持久化和实时热存储
"""
import requests
import json
import os
import time
from datetime import datetime


class IssuesCollector:
    """GitHub Issues全量采集器"""
    
    def __init__(self, repo, token=None):
        """
        初始化采集器
        
        Args:
            repo: 仓库名 owner/repo
            token: GitHub Token (可选，有token可获取更多)
        """
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.data_dir = 'data'
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.issues_file = os.path.join(self.data_dir, 'issues.json')
        self.prs_file = os.path.join(self.data_dir, 'pull_requests.json')
    
    def _load_existing(self, filepath):
        """加载已有数据（增量持久化）"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_realtime(self, data, filepath):
        """实时热存储"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def fetch_issues_search(self, state='all'):
        """
        使用Search API获取全部issues（不含PR）
        
        Search API每次最多1000条，需要按时间分段
        """
        existing = self._load_existing(self.issues_file)
        existing_numbers = {item['number'] for item in existing}
        
        all_issues = list(existing)
        page = 1
        
        query = f"repo:{self.repo} is:issue"
        if state != 'all':
            query += f" is:{state}"
        
        while True:
            url = f"{self.base_url}/search/issues"
            params = {
                'q': query,
                'per_page': 100,
                'page': page,
                'sort': 'created',
                'order': 'desc'
            }
            
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
                items = data.get('items', [])
                
                if not items:
                    break
                
                new_count = 0
                for item in items:
                    if item['number'] not in existing_numbers:
                        issue = {
                            'number': item['number'],
                            'title': item['title'],
                            'state': item['state'],
                            'author': item['user']['login'],
                            'created_at': item['created_at'],
                            'closed_at': item.get('closed_at'),
                            'labels': [l['name'] for l in item.get('labels', [])],
                            'comments': item.get('comments', 0)
                        }
                        all_issues.append(issue)
                        existing_numbers.add(item['number'])
                        new_count += 1
                
                self._save_realtime(all_issues, self.issues_file)
                
                total = data.get('total_count', 0)
                print(f"  获取第{page}页，累计{len(all_issues)}条 (总计约{total}条)")
                
                if len(all_issues) >= total or page >= 10:
                    break
                
                page += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"  ✗ 错误: {e}")
                break
        
        return all_issues
    
    def fetch_prs_search(self, state='all'):
        """使用Search API获取全部PRs"""
        existing = self._load_existing(self.prs_file)
        existing_numbers = {item['number'] for item in existing}
        
        all_prs = list(existing)
        page = 1
        
        query = f"repo:{self.repo} is:pr"
        if state != 'all':
            query += f" is:{state}"
        
        while True:
            url = f"{self.base_url}/search/issues"
            params = {
                'q': query,
                'per_page': 100,
                'page': page,
                'sort': 'created',
                'order': 'desc'
            }
            
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
                items = data.get('items', [])
                
                if not items:
                    break
                
                for item in items:
                    if item['number'] not in existing_numbers:
                        pr = {
                            'number': item['number'],
                            'title': item['title'],
                            'state': item['state'],
                            'author': item['user']['login'],
                            'created_at': item['created_at'],
                            'closed_at': item.get('closed_at'),
                            'labels': [l['name'] for l in item.get('labels', [])],
                            'merged': 'merged' in [l['name'].lower() for l in item.get('labels', [])]
                        }
                        all_prs.append(pr)
                        existing_numbers.add(item['number'])
                
                self._save_realtime(all_prs, self.prs_file)
                
                total = data.get('total_count', 0)
                print(f"  获取第{page}页，累计{len(all_prs)}条 (总计约{total}条)")
                
                if len(all_prs) >= total or page >= 10:
                    break
                
                page += 1
                time.sleep(2)
                
            except Exception as e:
                print(f"  ✗ 错误: {e}")
                break
        
        return all_prs
    
    def fetch_issues(self, state='all'):
        """兼容旧接口"""
        return self.fetch_issues_search(state)
    
    def fetch_pull_requests(self, state='all'):
        """兼容旧接口"""
        return self.fetch_prs_search(state)
    
    def save_issues(self, issues, filename='issues.json'):
        """保存issues"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(issues)}条)")
    
    def save_prs(self, prs, filename='pull_requests.json'):
        """保存PRs"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(prs, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(prs)}条)")
