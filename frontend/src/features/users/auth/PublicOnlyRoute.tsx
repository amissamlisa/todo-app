import { Navigate } from "react-router-dom";
import { useAuth } from "./useAuth";
import type { RouteProps } from "../types/router";

export const PublicOnlyRoute = ({ children }: RouteProps) => {
  const { token,isRehydrating } = useAuth();
  if (isRehydrating) return null;
  if (token) {
    return <Navigate to="/top" replace />;
  }
  return <>{children}</>;
};