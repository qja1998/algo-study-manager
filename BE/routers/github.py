from fastapi import APIRouter, HTTPException
from models.github import FolderCreateRequest, ReadmeUpdateRequest
from features.user import load_user_info
from features import github


router = APIRouter(prefix="/github", tags=["github"])


@router.post("/folders")
async def create_folders(request: FolderCreateRequest):
    """
    최종 확정된 문제 기준으로 디렉토리 생성
    """
    user_info = load_user_info()
    if not user_info:
        raise HTTPException(status_code=404, detail="User info not found. Please register user info first.")
    
    owner, repo = user_info.github_repo.split("/")
    results = []
    
    for folder_info in request.folders:
        path = folder_info.get("path")
        content = folder_info.get("content", "")
        message = folder_info.get("message", f"Add {path}")
        branch = folder_info.get("branch", "master")
        
        try:
            result = github.upsert_file(
                owner=owner,
                repo=repo,
                path=path,
                content_text=content,
                pat=user_info.github_pat,
                message=message,
                branch=branch
            )
            results.append({
                "path": path,
                "status": "success",
                "message": result.get("commit", {}).get("message", "")
            })
        except Exception as e:
            results.append({
                "path": path,
                "status": "error",
                "error": str(e)
            })
    
    return {"results": results}


@router.post("/readme")
async def update_readme(request: ReadmeUpdateRequest):
    """
    README.md에 문제 갱신
    """
    user_info = load_user_info()
    if not user_info:
        raise HTTPException(status_code=404, detail="User info not found. Please register user info first.")
    
    owner, repo = user_info.github_repo.split("/")
    
    try:
        result = github.upsert_file(
            owner=owner,
            repo=repo,
            path="README.md",
            content_text=request.content,
            pat=user_info.github_pat,
            message=request.message,
            branch=request.branch
        )
        return {
            "status": "success",
            "message": "README.md updated successfully",
            "commit": result.get("commit", {}).get("sha", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update README: {str(e)}")
