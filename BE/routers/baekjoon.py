from fastapi import APIRouter, HTTPException
from models.baekjoon import WorkbookUpdateRequest
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
        raise HTTPException(status_code=404, detail="User info not found. Please register user info first.")
    
    if not user_info.baekjoon_group_id:
        raise HTTPException(status_code=400, detail="Baekjoon group ID is not set")
    
    if not user_info.baekjoon_cookie:
        raise HTTPException(status_code=400, detail="Baekjoon cookie is not set")
    
    if not request.problem_ids:
        raise HTTPException(status_code=400, detail="At least one problem ID is required")
    
    try:
        workbook_id = baekjoon.create_workbook(
            group_id=user_info.baekjoon_group_id,
            workbook_name=request.workbook_name,
            workbook_description=request.workbook_description,
            problem_ids=request.problem_ids,
            bojautologin_value=user_info.baekjoon_cookie
        )
        
        return {
            "message": "Workbook created successfully",
            "workbook_id": workbook_id,
            "workbook_name": request.workbook_name,
            "problem_count": len(request.problem_ids)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workbook: {str(e)}")
