import { api } from './api';

//type을 명시하면 컴파일 후 이 줄이 사라짐.
import type { 
    postProblemRecommendRequest, 
    ProblemRecommendApiResponse 
} from '../types/problemSelect';

export const problemSelectApi = {
    // 문제 추천 요청
    // post<>로 타입을 선언할 수도 있으나 가독성을 위해 Promise<>로 선언.
    postProblemRecommend: (body: postProblemRecommendRequest): Promise<ProblemRecommendApiResponse> => {
        return api.post("/api/v1/problems/recommend", body);
    },

    // 문제 정보 조회
    getProblemInfo: () => {
        return api.get("/api/v1/problems/info");
    },

    // 문제 재추천
    postProblemReroll: () => {
        return api.post("/api/v1/problems/reroll");
    }
};