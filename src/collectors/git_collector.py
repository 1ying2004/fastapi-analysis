import subprocess

def get_commits(repo_path, max_count=10000):
    cmd = ['git', 'log', f'--max-count={max_count}', '--format=%H|%an|%ae|%ad|%s', '--date=iso']
    
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8', errors='replace')
    except subprocess.CalledProcessError as e:
        print(f"Error collecting commits: {e}")
        return []
    
    commits = []
    for line in output.strip().split('\n'):
        if '|' not in line:
            continue
        
        parts = line.split('|', 4)
        if len(parts) < 5:
            continue
        
        hash_val, author, email, date, msg = parts
        commits.append({
            'hash': hash_val,
            'author': author,
            'email': email,
            'date': date,
            'message': msg
        })
    
    print(f"Collected {len(commits)} commits")
    return commits
