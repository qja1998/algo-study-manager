from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from models.baekjoon import ProblemRecommendResponse, WorkbookUpdateRequest
from features.user import load_user_info
from features import baekjoon


router = APIRouter(prefix="/baekjoon", tags=["baekjoon"])


@router.post("/workbook")
async def create_workbook(request: WorkbookUpdateRequest):
    """
    새로운 문제집을 생성하고 추천된 문제를 추가합니다.
    """
    user_info = load_user_info()
    if not user_info:
        raise HTTPException(
            status_code=404,
            detail="User info not found. Please register user info first.",
        )

    if not user_info.baekjoon_group_id:
        raise HTTPException(status_code=400, detail="Baekjoon group ID is not set")

    if not user_info.baekjoon_cookie:
        raise HTTPException(status_code=400, detail="Baekjoon cookie is not set")

    if not request.problem_ids:
        raise HTTPException(
            status_code=400, detail="At least one problem ID is required"
        )

    try:
        workbook_id = baekjoon.create_workbook(
            group_id=user_info.baekjoon_group_id,
            workbook_name=request.workbook_name,
            workbook_description=request.workbook_description,
            problem_ids=request.problem_ids,
            bojautologin_value=user_info.baekjoon_cookie,
        )

        return {
            "message": "Workbook created successfully",
            "workbook_id": workbook_id,
            "workbook_name": request.workbook_name,
            "problem_count": len(request.problem_ids),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create workbook: {str(e)}"
        )


@router.get("/problems/recommend", response_model=ProblemRecommendResponse)
async def recommend_problems(
    minTier: int = Query(..., ge=1, le=30),
    maxTier: int = Query(..., ge=1, le=30),
    handle: Optional[str] = None,
    category: Optional[str] = None,
    minSolved: Optional[int] = Query(None, ge=0),
    minRate: Optional[float] = Query(None, ge=0),
    limit: int = Query(10, ge=1),
):
    """
    사용자가 설정한 필터 조건에 맞춰 문제 리스트를 반환합니다.
    (현재는 기능 구현 전이라 빈 결과를 반환합니다.)
    """
    return baekjoon.get_recommended_problems(
        handle=handle,
        min_tier=minTier,
        max_tier=maxTier,
        category=category,
        min_solved=minSolved,
        min_rate=minRate,
        limit=limit,
    )
