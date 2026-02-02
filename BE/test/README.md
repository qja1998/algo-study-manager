# BE 테스트

백엔드 API에 대한 유닛 테스트입니다.

## 설치

```bash
cd BE
pip install -r requirements.txt
```

## 테스트 실행

BE 폴더에서:

```bash
cd BE
pytest test/ -v
```

특정 테스트 파일만 실행:

```bash
pytest test/test_baekjoon_recommend.py -v
```

## 실제 API 동작 검증 (solved.ac 호출)

문제 추천이 실제로 solved.ac API를 호출해 결과를 반환하는지 확인하려면:

```bash
cd BE
python -m test.verify_recommend
# 또는 uv 사용 시
uv run python -m test.verify_recommend
```

성공 시 골드 구간(11~15) 문제 5개가 출력되고 exit code 0, 결과가 없거나 오류 시 1을 반환합니다. (네트워크 필요)

## 테스트 커버리지

현재 구현된 테스트:

### test_baekjoon_recommend.py
- 문제 추천 API (`GET /baekjoon/problems/recommend`) 테스트
- 필수/선택 파라미터 검증
- 파라미터 범위 검증 (tier: 1-30, limit: 1 이상 등)
- 응답 구조 검증
- 에러 케이스 검증 (422 Unprocessable Entity)
