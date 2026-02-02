from __future__ import annotations

from playwright.sync_api import sync_playwright
import requests

# selectors
EDIT_LINK_SELECTOR = "body > div.wrapper > div.container.content > div > div:nth-child(4) > blockquote > div > a"
INPUT_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-8 > div.form-group > div > input"
SUBMIT_BTN_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div.text-center.submit > button.btn.btn-primary"

# 문제집 생성 페이지 selectors
WORKBOOK_NAME_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div:nth-child(1) > div > input"
WORKBOOK_DESCRIPTION_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div:nth-child(2) > div > input"
PROBLEM_INPUT_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-8 > div.form-group > div > input"
CREATE_BTN_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div.text-center.submit > button"


def _tier_to_solvedac_format(tier: int) -> str:
    """
    백준 tier(1~30)를 solved.ac 쿼리 형식으로 변환합니다.

    예: 1 -> b5, 11 -> g5, 30 -> r1
    """
    if tier < 1 or tier > 30:
        raise ValueError("tier must be between 1 and 30")

    groups = [
        ("b", 1),  # Bronze
        ("s", 6),  # Silver
        ("g", 11),  # Gold
        ("p", 16),  # Platinum
        ("d", 21),  # Diamond
        ("r", 26),  # Ruby
    ]

    for prefix, start in groups:
        if start <= tier <= start + 4:
            offset = tier - start  # 0..4
            level = 5 - offset  # 5..1
            return f"{prefix}{level}"

    # unreachable
    raise ValueError("invalid tier")


def _extract_tag_names(tags) -> list[str]:
    """
    solved.ac 응답의 tags 형태(문자열 리스트 또는 객체 리스트)를
    내부 태그명 리스트로 정규화합니다.
    """
    if not tags:
        return []

    if isinstance(tags, list):
        if tags and isinstance(tags[0], str):
            return [t for t in tags if isinstance(t, str)]
        if tags and isinstance(tags[0], dict):
            names: list[str] = []
            for t in tags:
                if not isinstance(t, dict):
                    continue
                key = t.get("key") or t.get("name")
                if isinstance(key, str) and key:
                    names.append(key)
            return names

    return []


def create_workbook(
    group_id: str,
    workbook_name: str,
    workbook_description: str,
    problem_ids: list[str],
    bojautologin_value: str,
):
    """
    새로운 문제집을 생성하고 문제 추가

    Args:
        group_id: 백준 그룹 ID
        workbook_name: 문제집 이름
        workbook_description: 문제집 설명
        problem_ids: 문제 번호 리스트
        bojautologin_value: 백준 로그인 쿠키값

    Returns:
        생성된 문제집의 workbook_id (URL에서 추출)
    """
    create_url = f"https://www.acmicpc.net/group/workbook/create/{group_id}"
    # print(create_url)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # False 하면 창 띄우고 실행
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context()

        # 쿠키 주입
        context.add_cookies(
            [
                {
                    "name": "bojautologin",
                    "value": bojautologin_value,
                    "domain": ".acmicpc.net",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True,
                },
                # 있으면 넣어도 됨
                {
                    "name": "OnlineJudge",
                    "value": "OnlineJudge",
                    "domain": ".acmicpc.net",
                    "path": "/",
                },
            ]
        )

        page = context.new_page()

        # 1) 문제집 생성 페이지로 이동
        page.goto(create_url, wait_until="domcontentloaded")
        page.wait_for_timeout(500)

        # 로그인 체크(우회적)
        if "/login" in page.url:
            raise RuntimeError(
                "로그인 페이지로 이동했습니다. bojautologin 쿠키가 유효하지 않아요."
            )

        # 2) 문제집 이름 입력
        page.wait_for_selector(WORKBOOK_NAME_SELECTOR, timeout=10_000)
        page.fill(WORKBOOK_NAME_SELECTOR, workbook_name)
        page.wait_for_timeout(300)

        # 3) 문제집 설명 입력
        page.wait_for_selector(WORKBOOK_DESCRIPTION_SELECTOR, timeout=10_000)
        page.fill(WORKBOOK_DESCRIPTION_SELECTOR, workbook_description)
        page.wait_for_timeout(300)

        # 4) 문제 추가 (여러 개, 하나씩 입력 후 엔터)
        page.wait_for_selector(PROBLEM_INPUT_SELECTOR, timeout=10_000)
        for problem_id in problem_ids:
            page.click(PROBLEM_INPUT_SELECTOR)
            page.fill(PROBLEM_INPUT_SELECTOR, problem_id)
            page.keyboard.press("Enter")
            page.wait_for_timeout(300)  # 각 문제 추가 후 대기

        # 5) 문제집 생성 버튼 클릭
        page.wait_for_selector(CREATE_BTN_SELECTOR, timeout=10_000)
        page.click(CREATE_BTN_SELECTOR)

        # 생성 완료 대기
        page.wait_for_timeout(2000)

        # 6) 생성된 문제집의 workbook_id 추출 (리다이렉트된 URL에서)
        current_url = page.url
        if "/group/workbook/view/" in current_url:
            # URL 형식: https://www.acmicpc.net/group/workbook/view/{group_id}/{workbook_id}
            parts = current_url.split("/")
            workbook_id = parts[-1]
            return workbook_id
        else:
            raise RuntimeError(
                f"문제집 생성 실패: 예상치 못한 URL로 이동했습니다. ({current_url})"
            )


def add_problem(
    group_id: str, workbook_id: str, problem_id: str, bojautologin_value: str
):
    view_url = f"https://www.acmicpc.net/group/workbook/view/{group_id}/{workbook_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # False 하면 창 띄우고 실행
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context()

        # 쿠키 주입 (도메인 주의!)
        context.add_cookies(
            [
                {
                    "name": "bojautologin",
                    "value": bojautologin_value,
                    "domain": ".acmicpc.net",
                    "path": "/",
                    "httpOnly": True,
                    "secure": True,
                },
                # 있으면 넣어도 됨
                {
                    "name": "OnlineJudge",
                    "value": "OnlineJudge",
                    "domain": ".acmicpc.net",
                    "path": "/",
                },
            ]
        )

        page = context.new_page()

        # 1) 문제집 view 페이지로 이동
        page.goto(view_url, wait_until="domcontentloaded")
        page.wait_for_timeout(500)

        # 로그인 체크(우회적)
        if "/login" in page.url:
            raise RuntimeError(
                "로그인 페이지로 이동했습니다. bojautologin 쿠키가 유효하지 않아요."
            )

        # 2) 수정 페이지로 들어가는 링크 클릭
        page.wait_for_selector(EDIT_LINK_SELECTOR, timeout=10_000)
        page.click(EDIT_LINK_SELECTOR)

        # 3) 문제 번호 입력 + 엔터
        page.wait_for_selector(INPUT_SELECTOR, timeout=10_000)
        page.click(INPUT_SELECTOR)
        page.fill(INPUT_SELECTOR, problem_id)
        page.keyboard.press("Enter")

        # 4) 저장 버튼 클릭
        page.wait_for_selector(SUBMIT_BTN_SELECTOR, timeout=10_000)
        page.click(SUBMIT_BTN_SELECTOR)

        # 저장 반영 기다림
        page.wait_for_timeout(1200)

        # 5) 검증: 다시 view 페이지로 가서 problem 링크가 생겼는지 확인
        page.goto(view_url, wait_until="domcontentloaded")
        page.wait_for_timeout(800)

        html = page.content()
        ok = f"/problem/{problem_id}" in html

        if not ok:
            raise RuntimeError(
                f"문제 {problem_id} 추가 실패: 문제집에 반영되지 않았습니다."
            )

        return True


if __name__ == "__main__":
    BOJAUTOLOGIN_VALUE = ""

    GROUP_ID = ""
    WORKBOOK_ID = ""

    # 1) 단일 문제 추가 테스트
    add_problem(
        group_id=GROUP_ID,
        workbook_id=WORKBOOK_ID,
        problem_id="10034",
        bojautologin_value=BOJAUTOLOGIN_VALUE,
    )

    # 2) 문제집 생성 테스트
    new_wb_id = create_workbook(
        group_id=GROUP_ID,
        workbook_name="테스트 문제집",
        workbook_description="자동화 테스트",
        problem_ids=["1001", "1002", "1003"],
        bojautologin_value=BOJAUTOLOGIN_VALUE,
    )
    print("생성된 workbook_id:", new_wb_id)

    print("완료")


def get_recommended_problems(
    *,
    handle: str | None,
    min_tier: int,
    max_tier: int,
    category: str | None,
    min_solved: int | None,
    min_rate: float | None,
    limit: int,
):
    """
    사용자가 설정한 필터 조건에 맞춰 문제 리스트를 반환합니다.

    - 난이도 필터: solved.ac `*tier:min..max`
    - 태그 필터: OR 결합 (#tag1 | #tag2 ...)
    - 사용자가 푼 문제 제외: `!@handle`
    - 정렬: random
    - minRate: 응답 후 필터링
    """
    try:
        min_tier_q = _tier_to_solvedac_format(min_tier)
        max_tier_q = _tier_to_solvedac_format(max_tier)

        query = f"*tier:{min_tier_q}..{max_tier_q}"

        # 태그 OR 필터
        if category:
            tags = [t.strip() for t in category.split(",") if t.strip()]
            if tags:
                tag_or = " | ".join([f"#{t}" for t in tags])
                query += f" {tag_or}"

        # 최소 풀이자 수
        if min_solved is not None and min_solved > 0:
            query += f" s#{min_solved}.."

        # 사용자 제외 (푼 문제 제외)
        if handle:
            query += f" !@{handle}"

        url = "https://solved.ac/api/v3/search/problem"
        params = {"query": query, "sort": "random", "page": 1}
        headers = {"Accept": "application/json"}

        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        payload = resp.json() or {}
        items = payload.get("items") or []

        results = []
        for item in items:
            if not isinstance(item, dict):
                continue

            problem_id = item.get("problemId")
            if not isinstance(problem_id, int):
                continue

            title = item.get("titleKo") or item.get("title") or ""
            if not isinstance(title, str):
                title = str(title)

            tier = item.get("level")
            if not isinstance(tier, int):
                tier = min_tier

            solved_count = item.get("solvedCount")
            if not isinstance(solved_count, int):
                solved_count = item.get("acceptedUserCount")
            if not isinstance(solved_count, int):
                solved_count = 0

            try_count = item.get("tryCount")
            if not isinstance(try_count, int):
                try_count = item.get("submitCount")
            if not isinstance(try_count, int) or try_count <= 0:
                try_count = max(solved_count * 2, 1)

            acceptance_rate = (solved_count / try_count) * 100.0 if try_count else 0.0

            tag_names = _extract_tag_names(item.get("tags"))

            problem_obj = {
                "problemId": problem_id,
                "title": title,
                "tier": tier,
                "tags": tag_names,
                "stats": {
                    "solvedCount": solved_count,
                    "tryCount": try_count,
                    "acceptanceRate": float(acceptance_rate),
                },
                "constraints": {
                    "timeLimit": 1.0,
                    "memoryLimit": 256,
                },
                "url": f"https://www.acmicpc.net/problem/{problem_id}",
            }

            results.append(problem_obj)

        # minRate 필터링 (클라이언트 측)
        if min_rate is not None:
            results = [
                r
                for r in results
                if r.get("stats", {}).get("acceptanceRate", 0) >= min_rate
            ]

        results = results[:limit]
        return {"count": len(results), "data": results}

    except Exception:
        # solved.ac 호출 실패 등은 일단 빈 결과로 처리 (기존 동작 유지)
        return {"count": 0, "data": []}
