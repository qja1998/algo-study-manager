from pydantic import BaseModel
from typing import List


class WorkbookUpdateRequest(BaseModel):
    workbook_name: str  # 문제집 이름
    workbook_description: str  # 문제집 설명
    problem_ids: List[str]  # 문제 번호 리스트


class ProblemConstraints(BaseModel):
    timeLimit: float  # 초 단위
    memoryLimit: int  # MB 단위


class ProblemStats(BaseModel):
    solvedCount: int
    tryCount: int
    acceptanceRate: float


class ProblemItem(BaseModel):
    problemId: int
    title: str
    tier: int
    tags: List[str]
    stats: ProblemStats
    constraints: ProblemConstraints
    url: str


class ProblemRecommendResponse(BaseModel):
    count: int
    data: List[ProblemItem]
