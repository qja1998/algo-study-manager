"""
문제 추천 API (/baekjoon/problems/recommend) 유닛 테스트
"""

import sys
from pathlib import Path

# BE 폴더를 Python 경로에 추가
be_path = Path(__file__).parent.parent / "BE"
sys.path.insert(0, str(be_path))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRecommendProblems:
    """문제 추천 API 테스트"""

    def test_recommend_with_required_params_only(self):
        """필수 파라미터만 있는 경우 성공"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 15},
        )
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "data" in data
        assert data["count"] == 0
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0

    def test_recommend_with_all_params(self):
        """모든 파라미터가 있는 경우 성공"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={
                "minTier": 11,
                "maxTier": 15,
                "handle": "user123",
                "category": "dp,graph",
                "minSolved": 100,
                "minRate": 30.5,
                "limit": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "data" in data
        assert data["count"] == 0
        assert isinstance(data["data"], list)

    def test_recommend_with_custom_limit(self):
        """limit 파라미터 커스텀 값 테스트"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 1, "maxTier": 30, "limit": 20},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert isinstance(data["data"], list)

    def test_recommend_missing_min_tier(self):
        """minTier 파라미터 누락 시 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"maxTier": 15},
        )
        assert response.status_code == 422

    def test_recommend_missing_max_tier(self):
        """maxTier 파라미터 누락 시 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11},
        )
        assert response.status_code == 422

    def test_recommend_min_tier_below_range(self):
        """minTier가 1 미만일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 0, "maxTier": 15},
        )
        assert response.status_code == 422

    def test_recommend_min_tier_above_range(self):
        """minTier가 30 초과일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 31, "maxTier": 15},
        )
        assert response.status_code == 422

    def test_recommend_max_tier_below_range(self):
        """maxTier가 1 미만일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 0},
        )
        assert response.status_code == 422

    def test_recommend_max_tier_above_range(self):
        """maxTier가 30 초과일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 31},
        )
        assert response.status_code == 422

    def test_recommend_limit_below_minimum(self):
        """limit가 1 미만일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 15, "limit": 0},
        )
        assert response.status_code == 422

    def test_recommend_min_solved_negative(self):
        """minSolved가 음수일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 15, "minSolved": -1},
        )
        assert response.status_code == 422

    def test_recommend_min_rate_negative(self):
        """minRate가 음수일 때 422 에러"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 15, "minRate": -1.0},
        )
        assert response.status_code == 422

    def test_recommend_response_structure(self):
        """응답 구조 검증"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 11, "maxTier": 15},
        )
        assert response.status_code == 200
        data = response.json()

        # 최상위 필드 검증
        assert "count" in data
        assert "data" in data
        assert isinstance(data["count"], int)
        assert isinstance(data["data"], list)

        # 현재는 빈 결과만 반환하므로 data가 비어있어야 함
        assert data["count"] == 0
        assert len(data["data"]) == 0

    def test_recommend_with_category_comma_separated(self):
        """카테고리 파라미터가 쉼표로 구분된 경우"""
        response = client.get(
            "/baekjoon/problems/recommend",
            params={
                "minTier": 11,
                "maxTier": 15,
                "category": "dp,graph,math",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "data" in data

    def test_recommend_tier_range_edge_cases(self):
        """난이도 범위 경계값 테스트"""
        # 최소값
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 1, "maxTier": 1},
        )
        assert response.status_code == 200

        # 최대값
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 30, "maxTier": 30},
        )
        assert response.status_code == 200

        # 넓은 범위
        response = client.get(
            "/baekjoon/problems/recommend",
            params={"minTier": 1, "maxTier": 30},
        )
        assert response.status_code == 200
