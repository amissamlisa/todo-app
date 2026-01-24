import { Navigate } from "react-router-dom";
import { useAuth } from "./useAuth";


type PublicOnlyRouteProps = {
  children: React.ReactNode;
};

export const PublicOnlyRoute = ({ children }: PublicOnlyRouteProps) => {
  const { validateAccessToken } = useAuth();
  const isAuthenticated = validateAccessToken();

  if (isAuthenticated) {

    return <Navigate to="/top" replace />;
  }

  return <>{children}</>;
};