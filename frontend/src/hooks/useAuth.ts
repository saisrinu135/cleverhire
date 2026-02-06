import { useState } from 'react';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';
import { authService } from '@/services/authService';
import { LoginRequest, SignupRequest } from '@/types/auth';
import { sign } from 'crypto';

export const useAuth = () => {
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const login = async (data: LoginRequest) => {
        setIsLoading(true)

        try {
            const response = await authService.login(data);
            console.log(response)

            if (response.status_code == 200 && response.status && response.access) {
                localStorage.setItem('accessToken', response.access);
                localStorage.setItem('refreshToken', response.refresh);
                localStorage.setItem('user', JSON.stringify(response.user));

                toast.success(response?.message || 'Login Successful');
                router.push('/dashboard');
            } else {
                toast.error(response?.message || 'Login Failed');
            }
        } catch (err: any) {
            toast.error(err.response?.data?.message || "Login failed")
        } finally {
            setIsLoading(false);
        }
    };

    const signup = async (data: SignupRequest) => {
        setIsLoading(true);

        try {
            const response = await authService.signup(data);
            if (response.status_code == 201 && response.status) {
                toast.success(response?.message || 'Signup Successful. Please verify your email before logging in.');
            } else {
                toast.error(response?.message || 'Signup Failed');
            }
        } catch (err: any) {
            toast.error(err.response?.data?.message || 'Signup failed')
        } finally {
            setIsLoading(false)
        }
    };

    return {login, signup, isLoading };
};