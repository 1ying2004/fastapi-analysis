import requests
import time

class GitHubAPI:
    def __init__(self, repo, token=None):
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.token = token
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_issues(self, state='all', max_pages=10):
        url = f"{self.base_url}/repos/{self.repo}/issues"
        params = {'state': state, 'per_page': 100}
        
        all_issues = []
        page = 1
        
        while page <= max_pages:
            params['page'] = page
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                break
            
            issues = response.json()
            if not issues:
                break
            
            all_issues.extend(issues)
            page += 1
            time.sleep(0.5)
        
        print(f"Collected {len(all_issues)} issues")
        return all_issues
