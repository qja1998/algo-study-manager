from pydantic import BaseModel
from typing import Optional


class UserInfo(BaseModel):
    github_pat: str
    github_repo: str  # owner/repo 형식
    baekjoon_group_id: str
    baekjoon_workbook_id: Optional[str] = None
    baekjoon_cookie: Optional[str] = None  # bojautologin 쿠키

class UserInfoResponse(BaseModel):
    github_repo: str
    baekjoon_group_id: str
    baekjoon_workbook_id: Optional[str] = None
