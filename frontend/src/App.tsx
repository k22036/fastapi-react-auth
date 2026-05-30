import { useState } from "react";
import { AuthProvider } from "./contexts/AuthProvider";
import { useAuth } from "./hooks/useAuth";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import HomePage from "./pages/HomePage";

type Page = "signin" | "signup";

function AppContent() {
  const { isAuthenticated } = useAuth();
  const [page, setPage] = useState<Page>("signin");

  if (isAuthenticated) {
    return <HomePage />;
  }

  if (page === "signup") {
    return <SignUpPage onNavigateToSignIn={() => setPage("signin")} />;
  }

  return <SignInPage onNavigateToSignUp={() => setPage("signup")} />;
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
