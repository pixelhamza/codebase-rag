import json
import requests


def fetch_issues(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    response = requests.get(
        url,
        params={
            "state": "all",
            "per_page": 100
        }
    )
    response.raise_for_status()

    return response.json()

def save_issues(issues, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        for issue in issues:

            #Skip pull requests (GitHub returns them in the issues endpoint)
            if "pull_request" in issue:
                continue

            data = {
                "number": issue["number"],
                "title": issue["title"],
                "body": issue["body"],
                "url": issue["html_url"],
                "labels": [label["name"] for label in issue["labels"]]
            }

            f.write(json.dumps(data) + "\n")


if __name__ == "__main__":
    owner = "encode"
    repo = "httpx"

    issues = fetch_issues(owner, repo)

    save_issues(
        issues,
        "data/issues.jsonl"
    )

    print(f"Saved {len(issues)} issues.")