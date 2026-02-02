import os
from typing import Optional
from dotenv import load_dotenv, set_key, find_dotenv
from models.user import UserInfo

# 환경 변수 파일 경로 찾기
ENV_FILE = find_dotenv() or ".env"


def load_user_info() -> Optional[UserInfo]:
    """사용자 정보 로드"""
    load_dotenv()

    github_pat = os.getenv("GITHUB_PAT")
    github_repo = os.getenv("GITHUB_REPO")
    baekjoon_group_id = os.getenv("BAEKJOON_GROUP_ID")

    if not github_pat or not github_repo or not baekjoon_group_id:
        return None

    return UserInfo(
        github_pat=github_pat,
        github_repo=github_repo,
        baekjoon_group_id=baekjoon_group_id,
        baekjoon_workbook_id=os.getenv("BAEKJOON_WORKBOOK_ID"),
        baekjoon_cookie=os.getenv("BAEKJOON_COOKIE")
    )


def save_user_info(user_info: UserInfo):
    """사용자 정보 저장"""
    set_key(ENV_FILE, "GITHUB_PAT", user_info.github_pat)
    set_key(ENV_FILE, "GITHUB_REPO", user_info.github_repo)
    set_key(ENV_FILE, "BAEKJOON_GROUP_ID", user_info.baekjoon_group_id)

    if user_info.baekjoon_workbook_id:
        set_key(ENV_FILE, "BAEKJOON_WORKBOOK_ID", user_info.baekjoon_workbook_id)
    else:
        set_key(ENV_FILE, "BAEKJOON_WORKBOOK_ID", "")

    if user_info.baekjoon_cookie:
        set_key(ENV_FILE, "BAEKJOON_COOKIE", user_info.baekjoon_cookie)
    else:
        set_key(ENV_FILE, "BAEKJOON_COOKIE", "")

    # 환경 변수 다시 로드
    load_dotenv(override=True)
