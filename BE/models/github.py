from pydantic import BaseModel
from typing import Optional, List


class FolderCreateRequest(BaseModel):
    folders: List[dict]  # [{"path": "S3/week1/1000.py", "content": "code"}]

class ReadmeUpdateRequest(BaseModel):
    content: str
    branch: Optional[str] = "master"
    message: Optional[str] = "Update README"
