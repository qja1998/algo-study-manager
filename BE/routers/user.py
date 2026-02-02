from fastapi import APIRouter, HTTPException
from models.user import UserInfo, UserInfoResponse
from features.user import load_user_info, save_user_info


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/info")
async def create_or_update_user_info(user_info: UserInfo):
    """
    사용자 연동 인증 정보 등록/수정
    """
    save_user_info(user_info)
    return {
        "message": "User info saved successfully",
        "github_repo": user_info.github_repo,
        "baekjoon_group_id": user_info.baekjoon_group_id
    }


@router.get("/info")
async def get_user_info():
    """
    사용자 연동 인증 정보 조회
    """
    user_info = load_user_info()
    if not user_info:
        raise HTTPException(status_code=404, detail="User info not found")
    
    return UserInfoResponse(
        github_repo=user_info.github_repo,
        baekjoon_group_id=user_info.baekjoon_group_id,
        baekjoon_workbook_id=user_info.baekjoon_workbook_id
    )
