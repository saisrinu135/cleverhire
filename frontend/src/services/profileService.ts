import apiClient from '@/lib/api';
import { Profile, Education, Experience } from '@/types/profile';

export const profileService = {
    getProfile: async (): Promise<Profile> => {
        const response = await apiClient.get('/users/get-profile');
        return response.data;
    },

    getEducation: async (): Promise<Education> => {
        const response = await apiClient.get('/users/education');
        return response.data;
    },

    getExperience: async (): Promise<Experience> => {
        const response = await apiClient.get('/users/experience');
        return response.data;
    }
};
