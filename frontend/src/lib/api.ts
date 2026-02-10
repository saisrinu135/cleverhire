import axios, { AxiosRequestConfig } from "axios";
import { refresh } from "next/cache";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL
const APIVERSION = process.env.NEXT_PUBLIC_API_VERSION
const baseUrl = `${API_BASE_URL}/api/v1/${APIVERSION}`

// JWT utilities
const isTokenExpired = (token: string): boolean => {
    try {
        const  payload = JSON.parse(atob(token.split('.')[1]));
        // Check if the token will expire in next 5 mins
        return payload.exp * 1000 < Date.now() + 3000000;
    } catch {
        return true;
    }
};


const apiClient = axios.create({
    baseURL: `${API_BASE_URL}/api/${APIVERSION}`,
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to request if found in the localstorage
apiClient.interceptors.request.use(async (config) => {
    if (typeof window !== 'undefined') {
        if (config.url?.includes('/users/refresh')) {
            return config;
        }

        let token = localStorage.getItem('accessToken');

        if (token && isTokenExpired(token)) {
            try {
                const refreshToken = localStorage.getItem('refreshToken');

                if (!refreshToken) {
                    throw new Error('No refresh token available')
                }

                const response = await axios.post(`${API_BASE_URL}/${APIVERSION}/users/refresh`, {
                    refresh: refreshToken
                });

                token = response.data.access;
                localStorage.setItem('accessToken', token || '');
                localStorage.setItem('refreshToken', response.data.refresh)
            } catch {
                localStorage.clear();
                window.location.href = '/login';
                return Promise.reject('Token refresh failed')
            }
        }

        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
    }
    return config
});

// handle auth errors
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status_code === 401 && typeof window != 'undefined'){
            localStorage.clear();
            window.location.href = '/login';
        }
        return Promise.reject(error)
    }
)


export default apiClient;