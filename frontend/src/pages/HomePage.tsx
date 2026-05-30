import { useState } from "react";
import { signOut } from "../api/auth";
import { useAuth } from "../hooks/useAuth";

export default function HomePage() {
  const { token, email, clearToken } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSignOut = async () => {
    if (!token) return;
    setError(null);
    setIsLoading(true);

    try {
      await signOut(token);
      clearToken();
      // clearToken により isAuthenticated が false になり、
      // App.tsx のルーティングにより SignInPage へ遷移する
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "予期しないエラーが発生しました",
      );
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
      <div className="w-full max-w-sm bg-white dark:bg-gray-900 rounded-2xl shadow-lg p-8 text-center">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            <span className="text-3xl">👤</span>
          </div>
        </div>

        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">
          ようこそ
        </h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-8 break-all">
          {email}
        </p>

        {error && (
          <p
            role="alert"
            className="text-sm text-red-600 dark:text-red-400 mb-4"
          >
            {error}
          </p>
        )}

        <button
          onClick={handleSignOut}
          disabled={isLoading}
          className="w-full py-2 px-4 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-medium rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 disabled:opacity-50 transition-colors cursor-pointer"
        >
          {isLoading ? "サインアウト中..." : "サインアウト"}
        </button>
      </div>
    </div>
  );
}
