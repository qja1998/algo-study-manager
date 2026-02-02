import base64
import requests


API = "https://api.github.com"


def _headers(pat: str):
    return {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_file_sha(owner: str, repo: str, path: str, pat: str, branch: str="master") -> str | None:
    url = f"{API}/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=_headers(pat), params={"ref": branch}, timeout=10)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json().get("sha")


def upsert_file(owner: str, repo: str, path: str, content_text: str, pat: str,
                message: str, branch: str="master"):
    sha = get_file_sha(owner, repo, path, pat, branch)
    url = f"{API}/repos/{owner}/{repo}/contents/{path}"

    payload = {
        "message": message,
        "content": base64.b64encode(content_text.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha  # 수정일 때 필요

    r = requests.put(url, headers=_headers(pat), json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def test_repo_access(owner, repo, pat):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(url, headers=_headers(pat), timeout=10)
    print("status:", r.status_code)
    print("body:", r.json())


if __name__ == "__main__":
    owner = "Jeseoyun"
    repo = "repo-update-automation"
    pat = ""

    # test_repo_access(owner, repo, pat)

    # 1) 루트 README 갱신
    new_readme = "업데이트해주세요"
    upsert_file(owner, repo, "README.md", new_readme, pat, "Update README")

    # 2) 디렉토리 구조 생성/갱신 (폴더는 파일로 만든다)
    week1_text = "week 2 입니다"
    code_2210 = "codes"
    upsert_file(owner, repo, "S3/week2/.gitkeep", week1_text, pat, "Add week2 README")
    upsert_file(owner, repo, "S3/week2/23333.py", code_2210, pat, "Add solution 2210")
