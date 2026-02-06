import { UUID } from "crypto";

export interface ApiResponse<T = any> {
    status_code: number;
    message: string;
    status: string;
    data?: T;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface SignupRequest {
    email: string;
    password: string;
    first_name: string;
    last_name: string
}

export interface UserData {
    id: UUID;
    email: string;
    first_name: string;
    last_name: string;
    role: string;
    avatar: string;
    is_active: boolean;
    is_staff: boolean;
    is_superuser: boolean;
}

export interface LoginResponse {
    status_code: number;
    status: boolean;
    message: string;
    access: string;
    refresh: string;
    user: UserData;
}

export interface SignupResponseData {
    email: string;
    first_name: string;
    last_name: string;
    role: string;
}

export interface VerifyRequest {
    token: string
}

export interface LogutRequest {
    refresh: string
}

export type SignupResponse = ApiResponse<SignupResponseData>;