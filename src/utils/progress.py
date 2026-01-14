"""
进度显示
"""
import sys

class ProgressBar:
    def __init__(self, total, prefix='', length=50):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.current = 0
    
    def update(self, n=1):
        self.current += n
        percent = self.current / self.total
        filled = int(self.length * percent)
        bar = '█' * filled + '░' * (self.length - filled)
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent*100:.1f}%')
        sys.stdout.flush()
        
        if self.current >= self.total:
            print()
    
    def finish(self):
        self.current = self.total
        self.update(0)

def simple_progress(iterable, prefix='处理中'):
    """简单进度包装"""
    total = len(iterable)
    for i, item in enumerate(iterable):
        percent = (i + 1) / total * 100
        sys.stdout.write(f'\r{prefix}: {percent:.1f}%')
        sys.stdout.flush()
        yield item
    print()
