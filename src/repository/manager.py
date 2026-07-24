from pathlib import Path

from .utils import parse_github_url, repo_id

#determines where the cloned repo will live
class RepositoryManager:

    def __init__(self):
        self.base_dir = Path("data/repos")

    def prepare(self, github_url: str):
        owner, repo = parse_github_url(github_url)

        repository_id = repo_id(owner, repo)

        repo_dir = self.base_dir / repository_id

        return {
            "owner": owner,
            "repo": repo,
            "repo_id": repository_id,
            "directory": repo_dir,
        }