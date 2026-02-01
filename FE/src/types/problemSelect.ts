// Request 타입 정의
export interface postProblemRecommendRequest {
    count: number;
    filters: {
        tierMin: string;
        tierMax: string;
        tags: string[];
    };
}

// 공통 API 응답 타입
interface BaseApiResponse {
    ok: boolean;
}

// 성공 응답 타입
export interface postProblemRecommendResponse extends BaseApiResponse {
    ok: true;
    data: any; // 실제 문제 데이터 구조에 따라 구체적인 타입으로 변경 필요
}

// 에러 응답 타입
export interface ApiErrorResponse extends BaseApiResponse {
    ok: false;
    error: {
        message: string;
    };
}

// 전체 응답 타입 (성공 | 실패)
export type ProblemRecommendApiResponse = postProblemRecommendResponse | ApiErrorResponse;