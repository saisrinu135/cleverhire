"use client";

import { useEffect, useState } from "react";
import { profileService } from "@/services/profileService";
import { Profile, Education, Experience } from "@/types/profile";
import { User, MapPin, Phone, Briefcase, GraduationCap } from "lucide-react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [education, setEducation] = useState<Education | null>(null);
  const [experience, setExperience] = useState<Experience | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const [profileData, educationData, experienceData] = await Promise.all([
          profileService.getProfile(),
          profileService.getEducation(),
          profileService.getExperience()
        ]);
        setProfile(profileData);
        setEducation(educationData);
        setExperience(experienceData);
      } catch (error) {
        console.error("Failed to fetch profile", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
      </div>
    );
  }

  if (!profile?.data) return null;

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white p-4">
      <div className="max-w-4xl mx-auto py-8">
        {/* Header Section */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden mb-6">
          {/* Cover Image */}
          <div className="h-32 bg-gradient-to-r from-blue-500 to-purple-600">
            {profile.data.header && (
              <img
                src={profile.data.header}
                alt="Cover"
                className="w-full h-full object-cover"
              />
            )}
          </div>

          {/* Profile Info */}
          <div className="px-6 pb-6">
            <div className="flex items-start -mt-16 mb-4">
              <div className="relative">
                {profile.data.avatar ? (
                  <img
                    src={profile.data.avatar}
                    alt={profile.data.full_name}
                    className="w-32 h-32 rounded-full border-4 border-white shadow-lg object-cover"
                  />
                ) : (
                  <div className="w-32 h-32 rounded-full border-4 border-white shadow-lg bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center">
                    <User className="w-16 h-16 text-white" />
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-gray-900">
                {profile.data.full_name}
              </h1>

              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                {profile.data.location && (
                  <div className="flex items-center">
                    <MapPin className="w-4 h-4 mr-1" />
                    {profile.data.location}
                  </div>
                )}
                {profile.data.phone && (
                  <div className="flex items-center">
                    <Phone className="w-4 h-4 mr-1" />
                    {profile.data.phone}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Summary Section */}
        {profile.data.summary && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-3">About</h2>
            <p className="text-gray-700 leading-relaxed">{profile.data.summary}</p>
          </div>
        )}

        {/* Experience Section */}
        {experience?.data && experience.data.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
            <div className="flex items-center mb-4">
              <Briefcase className="w-5 h-5 text-blue-600 mr-2" />
              <h2 className="text-xl font-bold text-gray-900">Experience</h2>
            </div>
            <div className="space-y-6">
              {experience.data.map((exp) => (
                <div key={exp.id} className="border-l-2 border-blue-200 pl-4">
                  <h3 className="font-semibold text-gray-900">{exp.position}</h3>
                  <p className="text-blue-600 font-medium">{exp.company}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    {new Date(exp.start_date).toLocaleDateString("en-US", {
                      month: "short",
                      year: "numeric",
                    })}{" "}
                    -{" "}
                    {exp.is_current
                      ? "Present"
                      : new Date(exp.end_date!).toLocaleDateString("en-US", {
                          month: "short",
                          year: "numeric",
                        })}
                  </p>
                  {exp.location && (
                    <p className="text-sm text-gray-500">{exp.location}</p>
                  )}
                  {exp.description && (
                    <p className="text-gray-700 mt-2 text-sm">
                      {exp.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Education Section */}
        {education?.data && education.data.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center mb-4">
              <GraduationCap className="w-5 h-5 text-blue-600 mr-2" />
              <h2 className="text-xl font-bold text-gray-900">Education</h2>
            </div>
            <div className="space-y-6">
              {education.data.map((edu) => (
                <div key={edu.id} className="border-l-2 border-blue-200 pl-4">
                  <h3 className="font-semibold text-gray-900">
                    {edu.institution}
                  </h3>
                  <p className="text-blue-600 font-medium">
                    {edu.degree} in {edu.field_of_study}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    {new Date(edu.start_date).toLocaleDateString("en-US", {
                      month: "short",
                      year: "numeric",
                    })}{" "}
                    -{" "}
                    {edu.is_current
                      ? "Present"
                      : new Date(edu.end_date!).toLocaleDateString("en-US", {
                          month: "short",
                          year: "numeric",
                        })}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
