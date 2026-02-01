from pydantic import BaseModel
from typing import List


class WorkbookUpdateRequest(BaseModel):
    workbook_name: str  # 문제집 이름
    workbook_description: str  # 문제집 설명
    problem_ids: List[str]  # 문제 번호 리스트
