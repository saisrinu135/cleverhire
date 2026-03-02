import { UUID } from "crypto";
import { ApiResponse } from '@/types/auth'


export interface EducationData {
    id: UUID;
    institution: string;
    degree: string;
    field_of_study: string;
    start_date: string;
    end_date: string | null;
    is_current: boolean;
}

export interface ExperienceData {
    id: UUID;
    company: string;
    position: string;
    location: string;
    start_date: string;
    end_date: string | null;
    is_current: boolean;
    description: string;
}

export interface ProfileData {
    id: UUID;
    full_name: string;
    avatar: string | null;
    header: string | null;
    summary: string;
    phone: string;
    location: string;
}


export type Profile = ApiResponse<ProfileData>;
export type Education = ApiResponse<EducationData[]>;
export type Experience = ApiResponse<ExperienceData[]>;