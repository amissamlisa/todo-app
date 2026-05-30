import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./useAuth";
import type { RouteProps } from "../types/router";

export const PublicOnlyRoute = ({ children }: RouteProps) => {
  const { token,isRehydrating } = useAuth();
  const location = useLocation();
  const isPasswordResetPath = location.pathname === "/password-reset";

  if (isRehydrating) return null;
  if (token && !isPasswordResetPath) {
    return <Navigate to="/top" replace />;
  }
  return <>{children}</>;
};