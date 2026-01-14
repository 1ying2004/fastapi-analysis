"""
pysnooper动态追踪分析
实际使用pysnooper进行运行时代码追踪
"""
import pysnooper
import io
import sys
import os

TRACE_OUTPUT_DIR = 'traces'

@pysnooper.snoop(depth=2)
def traced_commit_analyzer(commits):
    """带追踪的提交分析"""
    result = {
        'total': 0,
        'authors': {},
        'types': {}
    }
    
    for commit in commits:
        result['total'] += 1
        
        author = commit.get('author', 'Unknown')
        result['authors'][author] = result['authors'].get(author, 0) + 1
        
        msg = commit.get('message', '')
        if msg.startswith('feat'):
            commit_type = 'feature'
        elif msg.startswith('fix'):
            commit_type = 'bugfix'
        else:
            commit_type = 'other'
        
        result['types'][commit_type] = result['types'].get(commit_type, 0) + 1
    
    return result

def trace_function(func, *args, output_file=None, **kwargs):
    """动态追踪任意函数执行"""
    os.makedirs(TRACE_OUTPUT_DIR, exist_ok=True)
    
    if output_file is None:
        output_file = os.path.join(TRACE_OUTPUT_DIR, f"{func.__name__}_trace.log")
    
    string_io = io.StringIO()
    
    @pysnooper.snoop(output=string_io, depth=3)
    def wrapped():
        return func(*args, **kwargs)
    
    result = wrapped()
    
    trace_output = string_io.getvalue()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== 函数追踪: {func.__name__} ===\n\n")
        f.write(trace_output)
    
    print(f"✓ 追踪日志: {output_file}")
    
    return result, trace_output

def analyze_trace_output(trace_text):
    """分析追踪输出"""
    lines = trace_text.split('\n')
    
    stats = {
        'total_lines': len(lines),
        'variable_changes': 0,
        'function_calls': 0,
        'returns': 0
    }
    
    for line in lines:
        if '...' in line and '=' in line:
            stats['variable_changes'] += 1
        if 'call' in line.lower():
            stats['function_calls'] += 1
        if 'return' in line.lower():
            stats['returns'] += 1
    
    return stats

class TracedAnalyzer:
    """带追踪的分析器类"""
    
    def __init__(self, enable_trace=True):
        self.enable_trace = enable_trace
        self.trace_buffer = io.StringIO()
    
    @pysnooper.snoop(depth=1)
    def analyze_complexity(self, code_lines):
        """分析代码复杂度"""
        complexity = 1
        
        for line in code_lines:
            line = line.strip()
            if line.startswith(('if ', 'elif ', 'for ', 'while ')):
                complexity += 1
            if ' and ' in line or ' or ' in line:
                complexity += 1
        
        return complexity
    
    @pysnooper.snoop(depth=1)
    def count_patterns(self, code_lines, patterns):
        """统计模式出现次数"""
        counts = {p: 0 for p in patterns}
        
        for line in code_lines:
            for pattern in patterns:
                if pattern in line:
                    counts[pattern] += 1
        
        return counts

def demo_pysnooper():
    """pysnooper演示"""
    print("=== pysnooper 动态追踪演示 ===\n")
    
    sample_commits = [
        {'author': 'Alice', 'message': 'feat: add feature'},
        {'author': 'Bob', 'message': 'fix: bug fix'},
        {'author': 'Alice', 'message': 'feat: another feature'}
    ]
    
    print("输入数据:", sample_commits)
    print("\n开始追踪...\n")
    
    result = traced_commit_analyzer(sample_commits)
    
    print("\n分析结果:", result)
    return result

if __name__ == '__main__':
    demo_pysnooper()
