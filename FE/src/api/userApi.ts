import {api} from './api';

export const useApi = {
    postUserInfo: () => {
        return api.post("/api/v1/users/info");
    },
    getUserInfo: () => {
        return api.get("/api/v1/users/info");
    },
    getMemberInfo: () => {
        return api.get("/api/v1/baekjoon/members");
    },
    getMemberSolves: () => {
        return api.get("/api/v1/baekjoon/solves");
    },
}