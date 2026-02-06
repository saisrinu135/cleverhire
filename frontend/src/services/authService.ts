import apiClient from "@/lib/api";
import { LoginRequest, LoginResponse, SignupRequest, SignupResponse, VerifyRequest, LogutRequest } from "@/types/auth";

export const authService = {
    login: async (data: LoginRequest): Promise<LoginResponse> => {
        const response = await apiClient.post('users/login/', data);
        return response.data;
    },

    signup: async (data: SignupRequest): Promise<SignupResponse> => {
        const response = await apiClient.post('users/signup/', data);
        return response.data;
    },

    verify: async (data: VerifyRequest) => {
        const response = await apiClient.post('users/verify/', data);
        return response.data;
    },

    logout: async (data: LogutRequest)=> {
        const response = await apiClient.post('users/logout/', data);
        return response.data;
    }
}