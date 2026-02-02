from fastapi import FastAPI
from dotenv import load_dotenv
from routers import user, github, baekjoon
import uvicorn


# 환경 변수 로드
load_dotenv()

app = FastAPI(title="Algo Study Manager API", version="1.0.0")

# 라우터 등록
app.include_router(user.router)
app.include_router(github.router)
app.include_router(baekjoon.router)


@app.get("/")
async def root():
    print("hello")
    return {"message": "Algo Study Manager API", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
