"""
命令行接口
"""
import argparse
import sys
from src.main import main as run_analysis
from src.config import REPO_PATH

def create_parser():
    parser = argparse.ArgumentParser(
        description='FastAPI 仓库分析工具'
    )
    parser.add_argument(
        '-r', '--repo',
        default=REPO_PATH,
        help='仓库路径'
    )
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='输出目录'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='详细输出'
    )
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    print(f"仓库: {args.repo}")
    print(f"输出: {args.output}")
    
    run_analysis()

if __name__ == '__main__':
    main()
