from urllib.parse import urlparse


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Returns (owner, repo)

    Example:
    https://github.com/encode/httpx-> ("encode", "httpx")
    """

    parsed = urlparse(url)

    if parsed.netloc != "github.com":
        raise ValueError("Only GitHub repositories are supported.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repo = parts[1].replace(".git", "")

    return owner, repo


def repo_id(owner: str, repo: str) -> str:
    return f"{owner}_{repo}"