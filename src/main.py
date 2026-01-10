from src.collectors.git_collector import get_commits, save_to_csv
from src.config import REPO_PATH, DATA_DIR
import os

def main():
    print("=== FastAPI Analysis ===")
    print(f"Analyzing repository: {REPO_PATH}")
    
    if not os.path.exists(REPO_PATH):
        print(f"Error: Repository not found at {REPO_PATH}")
        return
    
    commits = get_commits(REPO_PATH)
    
    if commits:
        save_to_csv(commits, DATA_DIR)
        print(f"Analysis complete: {len(commits)} commits processed")
    else:
        print("No commits found")

if __name__ == '__main__':
    main()
