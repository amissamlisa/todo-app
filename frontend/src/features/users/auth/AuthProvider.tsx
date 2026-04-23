import { type AxiosInstance } from "axios";
import axios from "axios";
import { AuthContext } from "./authContext";
import { useAuthProvider } from "../hooks/useAuthProvider";
import type { AuthProviderProps } from "../types/auth";
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true
});

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const {
    login,
    logout,
    token,
    loginErrorMessageFromServer,
    sendPasswordResetEmail,
    canResetPassword,
    verifyPasswordResetLink,
    clearLoginErrorMessage,
    isRehydrating,
  } = useAuthProvider(api);

  if (isRehydrating) {
    return null;
  }
  else {
    return (
      <AuthContext.Provider value={{ login, logout, token, loginErrorMessageFromServer, sendPasswordResetEmail, canResetPassword, verifyPasswordResetLink, clearLoginErrorMessage, api, isRehydrating }}>
        {children}
      </AuthContext.Provider>
    );
  }
};