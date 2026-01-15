"""
Issues采集模块 - 完整版

支持重试机制、增量持久化、实时热存储
"""
import requests
import json
import os
import time
from datetime import datetime


class IssuesCollector:
    """GitHub Issues全量采集器"""
    
    def __init__(self, repo, token=None):
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
        """加载已有数据"""
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
    
    def _request_with_retry(self, url, params, max_retries=3):
        """带重试的请求"""
        for attempt in range(max_retries):
            try:
                resp = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code == 403:
                    reset_time = int(resp.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(reset_time - int(time.time()), 60)
                    if wait_time > 120:
                        print(f"  ⚠ API限流需等待{wait_time}秒，跳过采集")
                        return None
                    print(f"  ⚠ API限流，等待{wait_time}秒...")
                    time.sleep(wait_time)
                    continue
                elif resp.status_code == 422:
                    return None
                else:
                    print(f"  ⚠ 请求失败({resp.status_code})，重试{attempt+1}/{max_retries}")
                    time.sleep(5)
            except Exception as e:
                print(f"  ⚠ 网络错误: {e}，重试{attempt+1}/{max_retries}")
                time.sleep(5)
        return None
    
    def fetch_issues(self, state='all'):
        """使用REST API获取issues（更稳定）"""
        existing = self._load_existing(self.issues_file)
        existing_numbers = {item['number'] for item in existing}
        
        all_issues = list(existing)
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{self.repo}/issues"
            params = {'state': state, 'page': page, 'per_page': 100}
            
            data = self._request_with_retry(url, params)
            if data is None or not data:
                break
            
            new_count = 0
            for item in data:
                if 'pull_request' in item:
                    continue
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
            print(f"  获取第{page}页，累计{len(all_issues)}条issues")
            
            if len(data) < 100:
                break
            
            page += 1
            time.sleep(1)
        
        return all_issues
    
    def fetch_pull_requests(self, state='all'):
        """获取PRs"""
        existing = self._load_existing(self.prs_file)
        existing_numbers = {item['number'] for item in existing}
        
        all_prs = list(existing)
        page = 1
        
        while True:
            url = f"{self.base_url}/repos/{self.repo}/pulls"
            params = {'state': state, 'page': page, 'per_page': 100}
            
            data = self._request_with_retry(url, params)
            if data is None or not data:
                break
            
            for item in data:
                if item['number'] not in existing_numbers:
                    pr = {
                        'number': item['number'],
                        'title': item['title'],
                        'state': item['state'],
                        'author': item['user']['login'],
                        'created_at': item['created_at'],
                        'closed_at': item.get('closed_at'),
                        'merged_at': item.get('merged_at'),
                        'labels': [l['name'] for l in item.get('labels', [])]
                    }
                    all_prs.append(pr)
                    existing_numbers.add(item['number'])
            
            self._save_realtime(all_prs, self.prs_file)
            print(f"  获取第{page}页，累计{len(all_prs)}条PRs")
            
            if len(data) < 100:
                break
            
            page += 1
            time.sleep(1)
        
        return all_prs
    
    def save_issues(self, issues, filename='issues.json'):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(issues)}条)")
    
    def save_prs(self, prs, filename='pull_requests.json'):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(prs, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath} ({len(prs)}条)")
