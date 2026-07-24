from pathlib import Path
import subprocess
from src.ingest.chunk_code import build_chunks
from src.ingest.build_index import vector_indexing
from src.ingest.build_bm25_index import build_bm25

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
    def clone(self, github_url: str, repo_dir: Path):
        repo_path = self.get_repo_path(repo_dir)

        repo_dir.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "git",
                "clone",
                github_url,
                str(repo_path)
            ],
            check=True
        )

    def is_cloned(self, repo_dir: Path) -> bool:
        repo_path = self.get_repo_path(repo_dir)
        return repo_path.exists()

    def get_repo_path(self, repo_dir: Path) -> Path:

        return repo_dir / "repo"

    def ensure_repository(self, github_url: str):
        info = self.prepare(github_url)

        if not self.is_cloned(info["directory"]):
            print("Cloning repository...")
            self.clone(github_url, info["directory"])

        return self.get_repo_path(info["directory"])

    def is_indexed(self, repo_dir: Path) -> bool:
        return (
            (repo_dir / "chunks.jsonl").exists()
            and (repo_dir / "bm25.pkl").exists()
            and (repo_dir / "qdrant").exists()
        )

    def build_index(self, repo_dir: Path):
        repo_path = self.get_repo_path(repo_dir)

        print("Chunking repository...")
        build_chunks(repo_path, repo_dir)

        print("Building vector index...")
        vector_indexing(repo_dir)

        print("Building BM25 index...")
        build_bm25(repo_dir)

    def prepare_repository(self, github_url: str):
        info = self.prepare(github_url)

        if not self.is_cloned(info["directory"]):
            print("Cloning repository...")
            self.clone(github_url, info["directory"])

        if not self.is_indexed(info["directory"]):
            print("Indexing repository...")
            self.build_index(info["directory"])

        return info