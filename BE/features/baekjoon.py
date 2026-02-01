from playwright.sync_api import sync_playwright

# selectors
EDIT_LINK_SELECTOR = "body > div.wrapper > div.container.content > div > div:nth-child(4) > blockquote > div > a"
INPUT_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-8 > div.form-group > div > input"
SUBMIT_BTN_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div.text-center.submit > button.btn.btn-primary"

# 문제집 생성 페이지 selectors
WORKBOOK_NAME_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div:nth-child(1) > div > input"
WORKBOOK_DESCRIPTION_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div:nth-child(2) > div > input"
PROBLEM_INPUT_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-8 > div.form-group > div > input"
CREATE_BTN_SELECTOR = "body > div.wrapper > div.container.content > div.row > form > div.col-md-4 > div.text-center.submit > button"


def create_workbook(
    group_id: str,
    workbook_name: str,
    workbook_description: str,
    problem_ids: list[str],
    bojautologin_value: str
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
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context()

        # 쿠키 주입
        context.add_cookies([
            {
                "name": "bojautologin",
                "value": bojautologin_value,
                "domain": ".acmicpc.net",
                "path": "/",
                "httpOnly": True,
                "secure": True,
            },
            # 있으면 넣어도 됨
            {"name": "OnlineJudge", "value": "OnlineJudge", "domain": ".acmicpc.net", "path": "/"},
        ])

        page = context.new_page()

        # 1) 문제집 생성 페이지로 이동
        page.goto(create_url, wait_until="domcontentloaded")
        page.wait_for_timeout(500)

        # 로그인 체크(우회적)
        if "/login" in page.url:
            raise RuntimeError("로그인 페이지로 이동했습니다. bojautologin 쿠키가 유효하지 않아요.")

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
            raise RuntimeError(f"문제집 생성 실패: 예상치 못한 URL로 이동했습니다. ({current_url})")


def add_problem(group_id: str, workbook_id: str, problem_id: str, bojautologin_value: str):
    view_url = f"https://www.acmicpc.net/group/workbook/view/{group_id}/{workbook_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # False 하면 창 띄우고 실행
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context()

        # 쿠키 주입 (도메인 주의!)
        context.add_cookies([
            {
                "name": "bojautologin",
                "value": bojautologin_value,
                "domain": ".acmicpc.net",
                "path": "/",
                "httpOnly": True,
                "secure": True,
            },
            # 있으면 넣어도 됨
            {"name": "OnlineJudge", "value": "OnlineJudge", "domain": ".acmicpc.net", "path": "/"},
        ])

        page = context.new_page()

        # 1) 문제집 view 페이지로 이동
        page.goto(view_url, wait_until="domcontentloaded")
        page.wait_for_timeout(500)

        # 로그인 체크(우회적)
        if "/login" in page.url:
            raise RuntimeError("로그인 페이지로 이동했습니다. bojautologin 쿠키가 유효하지 않아요.")

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
            raise RuntimeError(f"문제 {problem_id} 추가 실패: 문제집에 반영되지 않았습니다.")

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
        bojautologin_value=BOJAUTOLOGIN_VALUE
    )

    # 2) 문제집 생성 테스트
    new_wb_id = create_workbook(
        group_id=GROUP_ID,
        workbook_name="테스트 문제집",
        workbook_description="자동화 테스트",
        problem_ids=["1001", "1002", "1003"],
        bojautologin_value=BOJAUTOLOGIN_VALUE
    )
    print("생성된 workbook_id:", new_wb_id)

    print("완료")
