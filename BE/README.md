# Algo Study Manager [Backend]

알고리즘 스터디를 관리하는 FastAPI 서버입니다.

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 값을 설정하세요:

```bash
cp .env.example .env
```

또는 직접 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# GitHub Personal Access Token
GITHUB_PAT=your_github_pat_here

# GitHub 저장소 (owner/repo 형식)
GITHUB_REPO=owner/repo

# 백준 그룹 ID
BAEKJOON_GROUP_ID=your_baekjoon_group_id

# 백준 bojautologin 쿠키값
BAEKJOON_COOKIE=your_baekjoon_cookie

```

**참고:** 환경 변수는 두 가지 방법으로 설정할 수 있습니다:
1. `.env` 파일에 직접 작성
2. `POST /user/info` API를 통해 등록 (자동으로 `.env` 파일에 저장됨)

### 3. 서버 실행

```bash
python main.py
```

또는 uvicorn을 직접 사용:

```bash
uvicorn main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.
