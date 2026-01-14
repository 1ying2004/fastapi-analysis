"""
GitHub API模块

本模块封装GitHub REST API调用，支持分页获取issues和contributors，
具有自动重试和限流处理功能。

主要功能：
- get_issues: 获取仓库issues
- get_contributors: 获取贡献者列表
- save_data: 保存数据到JSON
"""
import requests
import time
import json
import os


class GitHubAPI:
    """
    GitHub API客户端
    
    封装了对GitHub REST API的调用，支持：
    - 自动分页获取大量数据
    - API限流处理（429错误自动等待）
    - 可选的认证Token
    
    Attributes:
        repo: 仓库名称，格式为 owner/repo
        base_url: API基础URL
        headers: 请求头
    """
    
    def __init__(self, repo, token=None):
        """
        初始化API客户端
        
        Args:
            repo: 仓库名称，如 'tiangolo/fastapi'
            token: GitHub Token（可选，用于提高限额）
        """
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def _fetch_paginated(self, url, params, max_items=5000):
        """
        分页获取数据的内部方法
        
        Args:
            url: API端点URL
            params: 请求参数
            max_items: 最大获取数量
        
        Returns:
            所有获取到的数据列表
        """
        all_items = []
        page = 1
        
        while len(all_items) < max_items:
            params['page'] = page
            params['per_page'] = 100
            
            response = requests.get(url, params=params, headers=self.headers)
            
            # 处理限流
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
            time.sleep(0.3)  # 避免过快请求
        
        return all_items
    
    def get_issues(self, state='all'):
        """获取仓库的issues"""
        url = f"{self.base_url}/repos/{self.repo}/issues"
        return self._fetch_paginated(url, {'state': state})
    
    def get_contributors(self):
        """获取仓库贡献者列表"""
        url = f"{self.base_url}/repos/{self.repo}/contributors"
        return self._fetch_paginated(url, {})
    
    def save_data(self, data, filename, output_dir='data'):
        """保存数据到JSON文件"""
        os.makedirs(output_dir, exist_ok=True)
        filepath = f"{output_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ 保存: {filepath}")
