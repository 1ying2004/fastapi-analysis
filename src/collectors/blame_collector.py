"""
Git blame分析
"""
import subprocess

def get_blame_info(repo_path, filepath):
    """获取文件的blame信息"""
    cmd = ['git', 'blame', '--line-porcelain', filepath]
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8', errors='replace')
    except:
        return []
    
    blame = []
    current = {}
    
    for line in output.split('\n'):
        if line.startswith('author '):
            current['author'] = line[7:]
        elif line.startswith('author-time '):
            current['time'] = line[12:]
        elif line.startswith('\t'):
            current['line'] = line[1:]
            blame.append(current.copy())
            current = {}
    
    return blame

def get_file_authors(repo_path, filepath):
    """获取文件的所有作者"""
    blame = get_blame_info(repo_path, filepath)
    authors = {}
    
    for b in blame:
        author = b.get('author', 'Unknown')
        authors[author] = authors.get(author, 0) + 1
    
    return authors
