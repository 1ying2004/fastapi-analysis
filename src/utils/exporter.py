"""
导出模块 - 支持多种格式
"""
import csv
import json
import os

class Exporter:
    def __init__(self, output_dir='data'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def to_csv(self, data, filename):
        """导出CSV"""
        if not data:
            return
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✓ CSV: {filepath}")
    
    def to_json(self, data, filename):
        """导出JSON"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✓ JSON: {filepath}")
    
    def to_markdown(self, data, filename, title='数据报告'):
        """导出Markdown表格"""
        if not data:
            return
        
        filepath = os.path.join(self.output_dir, filename)
        headers = list(data[0].keys())
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f'# {title}\n\n')
            f.write('| ' + ' | '.join(headers) + ' |\n')
            f.write('| ' + ' | '.join(['---'] * len(headers)) + ' |\n')
            for row in data[:100]:  # 限制100行
                f.write('| ' + ' | '.join(str(row.get(h, '')) for h in headers) + ' |\n')
        
        print(f"✓ Markdown: {filepath}")
