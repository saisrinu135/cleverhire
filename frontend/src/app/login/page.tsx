import { LoginForm } from '@/components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-linear-to-b from-blue-50 to-white">
      <LoginForm />
    </div>
  );
}