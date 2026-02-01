import {api} from './api';

export const problemRegisterApi = {
    postProblemRegisterFolder: () => {
        return api.post("/api/v1/github/folders");
    },
    postProblemRegisterReadme: () => {
        return api.post("/api/v1/github/readme");
    },
    postProblemRegisterBaekjoon: () => {
        return api.post("/api/v1/baekjoon/workbook");
    }
}