// src/app/page.tsx

import { SignupForm } from "@/components/auth/SignupForm";

export default function SignupPage() {
  return (
    <div className="min-h-screen bg-linear-to-r from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <SignupForm />
    </div>
  );
}