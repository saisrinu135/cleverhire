import apiClient from "@/lib/api";
import { LoginRequest, LoginResponse, SignupRequest, SignupResponse, VerifyRequest, LogutRequest } from "@/types/auth";

export const authService = {
    login: async (data: LoginRequest): Promise<LoginResponse> => {
        try {
            const response = await apiClient.post('users/login/', data);
            return response.data;
        } catch (error: any) {
            throw error.response?.data || error;
        }
    },

    signup: async (data: SignupRequest): Promise<SignupResponse> => {
        try {
            const response = await apiClient.post('users/signup/', data);
            return response.data;
        } catch (error: any) {
            throw error.response?.data || error;
        }
    },

    verify: async (data: VerifyRequest) => {
        try {
            const response = await apiClient.post('users/verify/', data);
            return response.data;
        } catch (error: any) {
            throw error.response?.data || error;
        }
    },

    logout: async (data: LogutRequest) => {
        try {
            const response = await apiClient.post('users/logout/', data);
            return response.data;
        } catch (error: any) {
            throw error.response?.data || error;
        }
    }
}