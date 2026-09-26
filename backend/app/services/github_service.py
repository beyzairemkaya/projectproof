import re
import httpx

GITHUB_REPO_RE = re.compile(r"^https://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?/?$")

def parse_repo_url(repo_url: str) -> tuple[str, str]:
    match = GITHUB_REPO_RE.match(repo_url)
    if not match:
        raise ValueError("Only standard public GitHub repository URLs are supported.")
    return match.group(1), match.group(2)

async def fetch_readme(repo_url: str) -> str:
    owner, repo = parse_repo_url(repo_url)
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/readme",
            headers={"Accept": "application/vnd.github.raw+json"},
        )
        response.raise_for_status()
        return response.text

async def fetch_repo_tree(repo_url: str) -> list[str]:
    owner, repo = parse_repo_url(repo_url)
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        repo_response = await client.get(f"https://api.github.com/repos/{owner}/{repo}")
        repo_response.raise_for_status()
        default_branch = repo_response.json()["default_branch"]
        tree_response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}",
            params={"recursive": "1"},
        )
        tree_response.raise_for_status()
    return [item["path"] for item in tree_response.json().get("tree", []) if item.get("type") == "blob"]
