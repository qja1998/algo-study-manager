"""
문제 추천 API가 실제로 solved.ac를 호출해 결과를 반환하는지 검증하는 스크립트.

실행 방법 (BE 폴더가 현재 디렉터리이거나 PYTHONPATH에 포함되어 있어야 함):
  cd BE && python -m test.verify_recommend
  # 또는 프로젝트 루트에서
  PYTHONPATH=BE python BE/test/verify_recommend.py
"""

import json
import sys
from pathlib import Path

# BE 루트를 경로에 추가
_be_root = Path(__file__).resolve().parent.parent
if str(_be_root) not in sys.path:
    sys.path.insert(0, str(_be_root))

from features import baekjoon


def main() -> int:
    print("문제 추천 API 검증: solved.ac 실제 호출")
    print("파라미터: minTier=11, maxTier=15, limit=5")
    print("-" * 60)

    result = baekjoon.get_recommended_problems(
        handle=None,
        min_tier=11,
        max_tier=15,
        category=None,
        min_solved=None,
        min_rate=None,
        limit=5,
    )

    count = result.get("count", 0)
    data = result.get("data") or []

    print(f"count: {count}")
    print(f"data 길이: {len(data)}")
    print()

    if not data:
        print("결과 없음 (solved.ac 응답이 비어있거나 오류일 수 있음)")
        return 1

    for i, item in enumerate(data, 1):
        print(f"[{i}] problemId={item.get('problemId')} | tier={item.get('tier')}")
        title = (item.get("title") or "")[:50]
        if len(item.get("title") or "") > 50:
            title += "..."
        print(f"    title: {title}")
        print(f"    tags: {item.get('tags', [])}")
        stats = item.get("stats") or {}
        rate = stats.get("acceptanceRate")
        rate_str = f"{rate:.1f}%" if rate is not None else "N/A"
        print(
            f"    stats: solved={stats.get('solvedCount')}, "
            f"try={stats.get('tryCount')}, rate={rate_str}"
        )
        print(f"    url: {item.get('url', '')}")
        print()

    print("-" * 60)
    print("검증 완료: 응답 구조가 기대한 대로 반환됨")
    return 0


if __name__ == "__main__":
    sys.exit(main())
