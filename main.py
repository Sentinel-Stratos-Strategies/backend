from fastapi import FastAPI
from git import Repo
import os

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}

@app.get("/git/log")
def git_log(limit: int = 10):
    """
    Get the git log for the repository.
    
    Args:
        limit: Number of commits to return (default: 10)
    
    Returns:
        List of commits with hash, author, date, and message
    """
    try:
        # Get the repository path
        repo_path = os.path.dirname(os.path.abspath(__file__))
        repo = Repo(repo_path)
        
        # Get the commits
        commits = []
        for commit in repo.iter_commits(max_count=limit):
            commits.append({
                "hash": commit.hexsha,
                "short_hash": commit.hexsha[:7],
                "author": commit.author.name,
                "email": commit.author.email,
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message.strip()
            })
        
        return {"commits": commits, "count": len(commits)}
    except Exception:
        return {"error": "Failed to retrieve git log", "commits": [], "count": 0}
