import { Navigate } from "react-router-dom";
import { useAuth } from "./useAuth";

type ProtectedRouteProps = {
  children: React.ReactNode;
};

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { validateAccessToken } = useAuth();
  const isAuthenticated = validateAccessToken();

  if (!isAuthenticated) {
    return <Navigate to="/logout" replace />;
  }

  return <>{children}</>;
};
