"""
标签采集模块

获取Git仓库的标签信息。
"""
import subprocess


def get_tags(repo_path):
    """获取所有标签列表"""
    cmd = ['git', 'tag', '-l']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
    except:
        return []
    
    return [t.strip() for t in output.strip().split('\n') if t.strip()]


def get_tag_info(repo_path, tag):
    """获取标签详细信息"""
    cmd = ['git', 'show', tag, '--format=%H|%ai|%s', '-s']
    try:
        output = subprocess.check_output(cmd, cwd=repo_path, encoding='utf-8')
        parts = output.strip().split('|')
        if len(parts) >= 3:
            return {
                'tag': tag,
                'hash': parts[0],
                'date': parts[1],
                'message': parts[2]
            }
    except:
        pass
    return None


def get_all_tags_info(repo_path):
    """获取所有标签的详细信息"""
    tags = get_tags(repo_path)
    return [get_tag_info(repo_path, t) for t in tags if get_tag_info(repo_path, t)]
